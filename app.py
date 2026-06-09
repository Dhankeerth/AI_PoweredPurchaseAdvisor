
from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/analyze", methods=["POST"])
def analyze():
  
    query = request.form.get("query", "").strip()
    
    if not query:
        return redirect(url_for('home'))
    
    prompt = f"""You are an expert product requirement analysis agent.

Your job is to understand a user's product request and convert it into structured JSON.

Return ONLY valid JSON. No additional text, explanations, or markdown formatting.

Schema:
{{
    "category": "product category (e.g., Electronics, Fashion, Home Appliances)",
    "budget": "budget amount or range mentioned, or 'Not specified'",
    "purpose": "main use case or purpose",
    "important_features": ["feature1", "feature2", ...],
    "preferred_brands": ["brand1", "brand2", ...] or empty array if none mentioned
}}

User Request:
{query}

Return JSON only."""
    
    category = "Not specified"
    budget = "Not specified"
    purpose = "Not specified"
    important_features = []
    preferred_brands = []

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY_1stAccount')

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        print("WARNING: GEMINI_API_KEY not found. Gemini API calls will fail.")
        print("Set the environment variable before running the application.")


    model = genai.GenerativeModel('gemini-2.5-flash')
    
    
    try:
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is not configured")
        
        # Create a Gemini model instance
       
        





        # Send the prompt to Gemini and get the response
        response = model.generate_content(prompt)
        
        # Get the text from the response
        response_text = response.text.strip()


        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Parse the JSON string into a Python dictionary
        parsed_data = json.loads(response_text.strip())
        
        # Step 6: Extract the structured information
        category = parsed_data.get("category", "Not specified")
        budget = parsed_data.get("budget", "Not specified")
        purpose = parsed_data.get("purpose", "Not specified")
        important_features = parsed_data.get("important_features", [])
        preferred_brands = parsed_data.get("preferred_brands", [])
        
        # Ensure lists are actually lists
        if not isinstance(important_features, list):
            important_features = []
        if not isinstance(preferred_brands, list):
            preferred_brands = []
        


        session["category"] = category
        session["budget"] = budget
        session["purpose"] = purpose
        session["important_features"] = important_features
        session["preferred_brands"] = preferred_brands
        
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        error_message = "Gemini API is not properly configured. Please contact the administrator."
        return render_template("understanding.html", 
                             original_query=query,
                             category=category,
                             budget=budget,
                             purpose=purpose,
                             important_features=important_features,
                             preferred_brands=preferred_brands,
                             error=error_message)
    
    except json.JSONDecodeError as je:
        print(f"JSON Parse Error: {je}")
        print(f"Response text: {response_text}")
        error_message = "Failed to parse AI response. Please try again with a clearer description."
        return render_template("understanding.html",
                             original_query=query,
                             category=category,
                             budget=budget,
                             purpose=purpose,
                             important_features=important_features,
                             preferred_brands=preferred_brands,
                             error=error_message)
    
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {e}")
        error_message = "An error occurred while analyzing your requirements. Please try again."
        return render_template("understanding.html",
                             original_query=query,
                             category=category,
                             budget=budget,
                             purpose=purpose,
                             important_features=important_features,
                             preferred_brands=preferred_brands,
                             error=error_message)
    
    # Step 8: Render the understanding.html template with extracted data
    return render_template("understanding.html",
                         original_query=query,
                         category=category,
                         budget=budget,
                         purpose=purpose,
                         important_features=important_features,
                         preferred_brands=preferred_brands)



@app.route("/top_picks")
def top_picks():
   
    if "category" not in session:
        return redirect(url_for('home'))
    
    category = session.get("category", "Not specified")
    budget = session.get("budget", "Not specified")
    purpose = session.get("purpose", "Not specified")
    important_features = session.get("important_features", [])
    preferred_brands = session.get("preferred_brands", [])
    
    
    top_picks_list = []
    alternatives_list = []
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY_2ndAccount')

    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        print("WARNING: GEMINI_API_KEY not found. Gemini API calls will fail.")
        print("Set the environment variable before running the application.")


    model2= genai.GenerativeModel('gemini-2.5-flash')
   
    try:
        # Check if API key is configured
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is not configured")
      
        features_str = ", ".join(important_features) if important_features else "None specified"
        brands_str = ", ".join(preferred_brands) if preferred_brands else "None specified"
        
        prompt = f"""You are an expert product recommendation agent.

Recommend products based on the following requirements.

Category: {category}
Budget: {budget}
Purpose: {purpose}
Important Features: {features_str}
Preferred Brands: {brands_str}

Recommend exactly:
- 3 top picks
- 2 alternative recommendations

Return ONLY valid JSON. No additional text, explanations, or markdown formatting.

Schema:
{{
    "top_picks": [
        {{
            "name": "Product name",
            "price": "Price with currency",
            "reason": "Why this product matches the requirements"
        }},
        {{
            "name": "Product name",
            "price": "Price with currency",
            "reason": "Why this product matches the requirements"
        }},
        {{
            "name": "Product name",
            "price": "Price with currency",
            "reason": "Why this product matches the requirements"
        }}
    ],
    "alternatives": [
        {{
            "name": "Product name",
            "price": "Price with currency",
            "reason": "Why this is a good alternative"
        }},
        {{
            "name": "Product name",
            "price": "Price with currency",
            "reason": "Why this is a good alternative"
        }}
    ]
}}

Rules:
- top_picks must contain exactly 3 products
- alternatives must contain exactly 2 products
- stay close to budget
- prioritize preferred brands when appropriate
- include real products currently available in the market
- return JSON only"""

        # Create a Gemini model instance
   
        
        # Send the prompt to Gemini and get the response
        response = model2.generate_content(prompt)
        
        # Get the text from the response
        response_text = response.text.strip()
   


        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        

        parsed_data = json.loads(response_text.strip())
        
        # Extract the recommendations
        top_picks_list = parsed_data.get("top_picks", [])
        alternatives_list = parsed_data.get("alternatives", [])
        


        # Ensure lists are actually lists
        if not isinstance(top_picks_list, list):
            top_picks_list = []
        if not isinstance(alternatives_list, list):
            alternatives_list = []
        
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        error_message = "Gemini API is not properly configured. Please contact the administrator."
        # Render dashboard with error
        return render_template("dashboard.html",
                             top_picks=[],
                             alternatives=[],
                             error=error_message,
                             category=category,
                             budget=budget,
                             purpose=purpose)
    
    except json.JSONDecodeError as je:
        print(f"JSON Parse Error: {je}")
        print(f"Response text: {response_text}")
        error_message = "Failed to parse AI recommendations. Please try again."
        return render_template("dashboard.html",
                             top_picks=[],
                             alternatives=[],
                             error=error_message,
                             category=category,
                             budget=budget,
                             purpose=purpose)
    
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {e}")
        error_message = "An error occurred while generating recommendations. Please try again."
        return render_template("dashboard.html",
                             top_picks=[],
                             alternatives=[],
                             error=error_message,
                             category=category,
                             budget=budget,
                             purpose=purpose)
    
    # Step 4: Render the dashboard.html template with recommendations
   
    return render_template("dashboard.html",
                         top_picks=top_picks_list,
                         alternatives=alternatives_list)





@app.route("/productanalyse", methods=["POST"])
def product_analyse():
    if "category" not in session:
        return redirect(url_for('home'))
    
    product_name = request.form.get("product_name", "").strip()
    product_price = request.form.get("product_price", "").strip()
    product_reason = request.form.get("product_reason", "").strip()
    
    if not product_name:
        return redirect(url_for('top_picks'))
    category = session.get("category", "Not specified")
    budget = session.get("budget", "Not specified")
    purpose = session.get("purpose", "Not specified")
    important_features = session.get("important_features", [])
    preferred_brands = session.get("preferred_brands", [])

    features_str = ", ".join(important_features) if important_features else "None specified"
    brands_str = ", ".join(preferred_brands) if preferred_brands else "None specified"
    

    analysis = {
        "overall_match_percentage": "0",
        "budget_match": "0",
        "feature_match": "0",
        "brand_match": "0",
        "purpose_match": "0",
        "value_for_money": "Analysis not available",
        "pros": [],
        "cons": [],
        "final_verdict": "Analysis could not be generated."
    }
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY_1stAccount')
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)


    model = genai.GenerativeModel('gemini-2.5-flash')

    try:
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is not configured")
        prompt = f"""You are an expert product analysis agent.

Analyze how well the selected product matches the user's requirements.

USER REQUIREMENTS:
- Category: {category}
- Budget: {budget}
- Purpose: {purpose}
- Important Features: {features_str}
- Preferred Brands: {brands_str}

SELECTED PRODUCT:
- Name: {product_name}
- Price: {product_price}
- Recommendation Reason: {product_reason}

Compare the user requirements with the selected product and generate a detailed analysis.

Return ONLY valid JSON. No additional text, explanations, or markdown formatting.

Required JSON format:
{{
    "overall_match_percentage": "number between 0-100",
    "budget_match": "number between 0-100",
    "feature_match": "number between 0-100",
    "brand_match": "number between 0-100",
    "purpose_match": "number between 0-100",
    "value_for_money": "detailed analysis of value for money",
    "pros": ["pro1", "pro2", "pro3"],
    "cons": ["con1", "con2", "con3"],
    "final_verdict": "comprehensive final verdict"
}}

Rules:
- All percentage values must be numeric strings (e.g., "85" not "85%")
- the overall match percent can be calculated like how much the user requiremnt and the product are matching this mathcing percentage should be valid
- Provide at least 3 pros and 3 cons
- The final verdict should be 2-3 sentences
- Be objective and honest in your analysis
- Return JSON only, no markdown code blocks

"""
        response=model.generate_content(prompt)
        response_text=response.text.strip()

        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        parsed_data = json.loads(response_text.strip())

        analysis = {
            "overall_match_percentage": str(parsed_data.get("overall_match_percentage", "0")),
            "budget_match": str(parsed_data.get("budget_match", "0")),
            "feature_match": str(parsed_data.get("feature_match", "0")),
            "brand_match": str(parsed_data.get("brand_match", "0")),
            "purpose_match": str(parsed_data.get("purpose_match", "0")),
            "value_for_money": parsed_data.get("value_for_money", "Analysis not available"),
            "pros": parsed_data.get("pros", []),
            "cons": parsed_data.get("cons", []),
            "final_verdict": parsed_data.get("final_verdict", "Analysis could not be generated.")
        }

        if not isinstance(analysis["pros"], list):
            analysis["pros"] = []
        if not isinstance(analysis["cons"], list):
            analysis["cons"] = []
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
        error_message = "Gemini API is not properly configured."
        return render_template("product_analysis.html",
                             product={"name": product_name, "price": product_price, "reason": product_reason},
                             analysis=analysis,
                             error=error_message)
    
    except json.JSONDecodeError as je:
        print(f"JSON Parse Error: {je}")
        print(f"Response text: {response_text}")
        error_message = "Failed to parse AI analysis. Please try again."
        return render_template("product_analysis.html",
                             product={"name": product_name, "price": product_price, "reason": product_reason},
                             analysis=analysis,
                             error=error_message)
    
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {e}")
        error_message = "An error occurred while analyzing the product. Please try again."
        return render_template("product_analysis.html",
                             product={"name": product_name, "price": product_price, "reason": product_reason},
                             analysis=analysis,
                             error=error_message)
    product = {
        "name": product_name,
        "price": product_price,
        "reason": product_reason
    }
    
    return render_template("product_analysis.html",
                         product=product,
                         analysis=analysis)
    







if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5000)
