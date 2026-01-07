from django.shortcuts import render,redirect
from django.http import JsonResponse
import re
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import FacultySignUpForm, FacultyLoginForm
# Download NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('punkt_tab')  # This is the missing resource
nltk.download('omw-1.4')    # Often needed for WordNet

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Student data including all records
students = {
    "Abel SG": {
        "Class": "S7 CSE",
        "Father Name": "George",
        "Mother Name": "Sheela SG",
        "Attendance Percentage": "72%",
        "Curriculum Performance": "Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 6.897,
            "2nd Semester": 6.967,
            "3rd Semester": 6.909,
            "4th Semester": 7.567,
            "5th Semester": 7.966,
            "6th Semester": 7.009
        },
        "Feedback from FA": "He is a dedicated and responsible student who completes assignments on time.",
        "Assignment Marks": {
            "Operating System": 17,
            "Cryptography": 16,
            "Engineering Startup And Entrepreneur Management": 16,
            "Advanced Java Programming": 15,
            "Advanced Java Programming Lab": 17
        },
        "Fees Status": {
            "Semester Fees": "paid",
            "Bus Fees": "paid"
        },
        "Address": "VK House, Kottarakkara.P.O, Kollam, 691536",
        "Contact Details": {
            "Father": "9755126059",
            "Mother": "9896205555",
            "Student": "9847834455"
        }
    },
    "Safeer Bashar": {
        "Class": "S7 CSE",
        "Father Name": "Bashar V",
        "Mother Name": "Fathima V",
        "Attendance Percentage": "74%",
        "Curriculum Performance": "Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 6.934,
            "2nd Semester": 6.234,
            "3rd Semester": 6.908,
            "4th Semester": 6.455,
            "5th Semester": 6.966,
            "6th Semester": 7.098
        },
        "Feedback from FA": "Maintains discipline and follows classroom rules.",
        "Assignment Marks": {
            "Operating System": 17,
            "Cryptography": 15,
            "Engineering Startup And Entrepreneur Management": 16,
            "Advanced Java Programming": 14,
            "Advanced Java Programming Lab": 17
        },
        "Fees Status": {
            "Semester Fees": "paid",
            "Hostel Fees": "paid"
        },
        "Address": "Safaa Nivas, Kannur.P.O, Kannur, 670001",
        "Contact Details": {
            "Father": "8976776678",
            "Mother": "6098897775",
            "Student": "6799979993"
        }
    },
    "Jaibin Joe": {
        "Class": "S7 CSE",
        "Father Name": "Joe S",
        "Mother Name": "Sheeja Joe",
        "Attendance Percentage": "73%",
        "Curriculum Performance": "Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 6.678,
            "2nd Semester": 6.988,
            "3rd Semester": 6.342,
            "4th Semester": 6.666,
            "5th Semester": 6.980,
            "6th Semester": 6.565
        },
        "Feedback from FA": "Shows a good understanding of concepts and applies them adequately in class.",
        "Assignment Marks": {
            "Operating System": 15,
            "Cryptography": 14,
            "Engineering Startup And Entrepreneur Management": 13,
            "Advanced Java Programming": 11,
            "Advanced Java Programming Lab": 13
        },
        "Fees Status": {
            "Semester Fees": "paid",
            "Hostel Fees": "paid"
        },
        "Address": "JJ Cottage, Trissur.P.O, Trissur, 680001",
        "Contact Details": {
            "Father": "6655766777",
            "Mother": "7878878987",
            "Student": "9089788978"
        }
    },
    "Sahal TP": {
        "Class": "S7 CSE",
        "Father Name": "Abdhul TP",
        "Mother Name": "Kadheeja TP",
        "Attendance Percentage": "70%",
        "Curriculum Performance": "Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 6.646,
            "2nd Semester": 5.988,
            "3rd Semester": 6.342,
            "4th Semester": 6.112,
            "5th Semester": 5.988,
            "6th Semester": 6.098
        },
        "Feedback from FA": "Maintains discipline and follows classroom rules.",
        "Assignment Marks": {
            "Operating System": 17,
            "Cryptography": 13,
            "Engineering Startup And Entrepreneur Management": 10,
            "Advanced Java Programming": 11,
            "Advanced Java Programming Lab": 12
        },
        "Fees Status": {
            "Semester Fees": "not paid",
            "Hostel Fees": "not paid"
        },
        "Address": "Sahal Manzil, Thiruporur.P.O, Kancheepuram, 603110",
        "Contact Details": {
            "Father": "9877676657",
            "Mother": "9788868762",
            "Student": "7796868688"
        }
    },
    "Jeffin M": {
        "Class": "S7 CSE",
        "Father Name": "Edison",
        "Mother Name": "Jiji Edison",
        "Attendance Percentage": "59%",
        "Curriculum Performance": "Below Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 5.091,
            "2nd Semester": 4.988,
            "3rd Semester": 5.342,
            "4th Semester": 6.099,
            "5th Semester": 5.343,
            "6th Semester": 6.112
        },
        "Feedback from FA": "Struggles with grasping key concepts and needs additional support to reinforce learning.",
        "Assignment Marks": {
            "Operating System": 16,
            "Cryptography": 11,
            "Engineering Startup And Entrepreneur Management": 8,
            "Advanced Java Programming": 7,
            "Advanced Java Programming Lab": 12
        },
        "Fees Status": {
            "Semester Fees": "paid",
            "Bus Fees": "paid"
        },
        "Address": "Medayil House, Thiruporur.P.O, Kancheepuram, 603110",
        "Contact Details": {
            "Father": "8722552255",
            "Mother": "9867565412",
            "Student": "6757575744"
        }
    },
    "Subin S": {
        "Class": "S7 CSE",
        "Father Name": "Sojan",
        "Mother Name": "Mini Sojan",
        "Attendance Percentage": "55%",
        "Curriculum Performance": "Below Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 5.567,
            "2nd Semester": 4.657,
            "3rd Semester": 5.655,
            "4th Semester": 6.598,
            "5th Semester": 5.567,
            "6th Semester": 5.778
        },
        "Feedback from FA": "Shows limited engagement in class discussions and activities; needs to be more active in asking questions and sharing thoughts.",
        "Assignment Marks": {
            "Operating System": 13,
            "Cryptography": 10,
            "Engineering Startup And Entrepreneur Management": 9,
            "Advanced Java Programming": 8,
            "Advanced Java Programming Lab": 8
        },
        "Fees Status": {
            "Semester Fees": "not paid",
            "Bus Fees": "not paid"
        },
        "Address": "Subin Cottage, House no.65, Kelabakkam.P.O, Chengalpattu, 603001",
        "Contact Details": {
            "Father": "6788767674",
            "Mother": "6688899756",
            "Student": "8989978434"
        }
    },
    "John A": {
        "Class": "S7 CSE",
        "Father Name": "Andrew A",
        "Mother Name": "Jennifer Andrew",
        "Attendance Percentage": "55%",
        "Curriculum Performance": "Below Average",
        "On Duty Application": "Details available",
        "CGPA": {
            "1st Semester": 4.565,
            "2nd Semester": 5.656,
            "3rd Semester": 6.655,
            "4th Semester": 5.565,
            "5th Semester": 4.567,
            "6th Semester": 5.677
        },
        "Feedback from FA": "Struggles with grasping key concepts and needs additional support to reinforce learning.",
        "Assignment Marks": {
            "Operating System": 15,
            "Cryptography": 10,
            "Engineering Startup And Entrepreneur Management": 8,
            "Advanced Java Programming": 8,
            "Advanced Java Programming Lab": 5
        },
        "Fees Status": {
            "Semester Fees": "paid",
            "Bus Fees": "paid"
        },
        "Address": "JJ House, House no.52, Thiruporur.P.O, Kancheepuram, 603110",
        "Contact Details": {
            "Father": "9845677823",
            "Mother": "8564783888",
            "Student": "8885538140"
        }
    }
}

# Helper function to preprocess user input
def preprocess_input(user_input):
    tokens = word_tokenize(user_input.lower())
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

# Function to extract the student name from the input
def extract_student_name(user_input):
    user_input_lower = user_input.lower()
    for name in students.keys():
        if name.lower() in user_input_lower:
            return name
        # fallback: match by first name if possible
        first_name = name.split()[0].lower()
        if first_name in user_input_lower:
            return name
    return None

# Main chatbot response function
def chatbot_response(user_input):
    user_input_lower = user_input.lower()

    # Greetings
    if any(word in user_input_lower for word in ["hi", "hello", "hey", "greetings"]):
        return random.choice(["Hello! How can I assist you?", "Hi there! What can I do for you?"])

    # Goodbyes
    if any(word in user_input_lower for word in ["bye", "goodbye", "see you", "quit"]):
        return random.choice(["Goodbye! Have a great day!", "Bye! See you soon!"])

    # Thanks
    if any(word in user_input_lower for word in ["thanks", "thank you", "appreciate it"]):
        return random.choice(["You're welcome!", "Happy to help!", "No problem!"])

    tokens = preprocess_input(user_input)
    student_name = extract_student_name(user_input)
    
    if not student_name:
        return "I couldn't find the student. Please provide the student's name."
    
    student = students[student_name]

    # Attendance query
    if "attendance" in tokens:
        return f"{student_name}'s attendance percentage is {student['Attendance Percentage']}."

    # CGPA query
    if "cgpa" in tokens:
        semester = re.search(r"\d+(st|nd|rd|th)", user_input_lower)
        if semester:
            semester_key = f"{semester.group()} Semester"
            if semester_key in student["CGPA"]:
                return f"{student_name}'s CGPA in {semester_key} is {student['CGPA'][semester_key]}."
        return f"{student_name}'s CGPA across semesters: {student['CGPA']}."

    # Assignment marks query
    if "assignment" in tokens or "marks" in tokens:
        subject = re.search(r"operating system|cryptography|engineering startup and entrepreneur management|advanced java programming", user_input_lower)
        if subject:
            subject_key = subject.group().title()
            if subject_key in student["Assignment Marks"]:
                return f"{student_name}'s assignment marks in {subject_key} is {student['Assignment Marks'][subject_key]}."
        return f"{student_name}'s assignment marks: {student['Assignment Marks']}."

    # Fees status query
    if "fees" in tokens:
        fees_status = student["Fees Status"]
        response = f"{student_name}'s fees status: "
        if "Semester Fees" in fees_status:
            response += f"Semester Fees - {fees_status['Semester Fees']}, "
        if "Bus Fees" in fees_status:
            response += f"Bus Fees - {fees_status['Bus Fees']}, "
        if "Hostel Fees" in fees_status:
            response += f"Hostel Fees - {fees_status['Hostel Fees']}, "
        return response.rstrip(", ")

    # Address query
    if "address" in tokens:
        return f"{student_name}'s address is {student['Address']}."

    # Contact details query
    if "contact" in tokens or "phone" in tokens:
        contacts = student["Contact Details"]
        # Check if query mentions father or mother explicitly
        if "father" in tokens:
            return f"{student_name}'s father's phone number is {contacts['Father']}."
        elif "mother" in tokens:
            return f"{student_name}'s mother's phone number is {contacts['Mother']}."
        # Fallback: if no parent is mentioned, return student's phone number
        elif student_name.lower().split()[0] in tokens:
            return f"{student_name}'s phone number is {contacts['Student']}."
        else:
            return f"{student_name}'s contact details: {contacts}."

    # Feedback query
    if "feedback" in tokens:
        return f"{student_name}'s feedback from FA: {student['Feedback from FA']}."

    # Father's and Mother's Name queries (if not handled in contact)
    if "father" in tokens:
        return f"{student_name}'s father name is {student['Father Name']}."
    if "mother" in tokens:
        return f"{student_name}'s Mother name is {student['Mother Name']}."

    # Default response
    return "I didn't understand that. Can you please rephrase your query?"

# Django view to render the index page
def get_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        response = chatbot_response(user_input)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request method'})

# Faculty Signup View
def faculty_signup(request):
    if request.method == 'POST':
        form = FacultySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chatbot_page')
    else:
        form = FacultySignUpForm()
    return render(request, 'signup.html', {'form': form})

# Faculty Login View with improved error handling
def faculty_login(request):
    if request.method == 'POST':
        form = FacultyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    if user.is_active:
                        login(request, user)
                        next_url = request.GET.get('next', 'chatbot_page')
                        return redirect(next_url)
                    else:
                        return render(request, 'login.html', {'form': form, 'error': 'Account is inactive'})
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Incorrect password'})
            except User.DoesNotExist:
                return render(request, 'login.html', {'form': form, 'error': 'User does not exist'})
    else:
        form = FacultyLoginForm()
    return render(request, 'login.html', {'form': form})

# Faculty Logout View
def faculty_logout(request):
    logout(request)
    return redirect('faculty_login')

# Chatbot Page View (requires login)
@login_required
def chatbot_page(request):
    return render(request, 'index.html')