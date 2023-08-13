import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient
from bson import json_util
from bson import ObjectId

import re
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
smtp_email = os.environ.get('SMTP_EMAIL')
mongodb_connection = os.environ.get('MONGO_CONNECTION')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


client = MongoClient("mongodb://localhost:27017")
db = client["hrms"]
jobs_collection = db["jobs"]
applications_collection = db["applications"]
processed_applications_collection = db["processed_applications"]
interview_collection = db["interview"]



def get_interview_info(application_id):
    interview_info = {}
    
    try:
        # Convert application_id to ObjectId
        application_id = ObjectId(application_id)

        # Retrieve the candidate information from hrms.applications
        application_doc = applications_collection.find_one({"_id": application_id})
        if application_doc:
            interview_info['name'] = application_doc.get("Name", "")
            interview_info['resume_summary'] = application_doc.get("Resume_Summary", "")
            job_id = application_doc.get("Job_ID")

            # Convert job_id to ObjectId
            job_id = ObjectId(job_id)

            # Retrieve the job information from hrms.jobs
            job_doc = jobs_collection.find_one({"_id": job_id})
            if job_doc:
                interview_info['job'] = job_doc.get("Job", "")
                interview_info['job_description'] = job_doc.get("Job_Description", "")
                interview_info['company'] = job_doc.get("About_Company", "")
                interview_info['job_summary'] = job_doc.get("Job_Summary", "")

    except Exception as e:
        print("Error:", e)

    return interview_info


@csrf_exempt
def interview(request, application_id):
    if request.method == 'POST':
        # Fetch interview information from MongoDB based on application_id
        interview_info = get_interview_info(application_id)

        if not interview_info:
            # Return an error response if interview_info is empty
            return JsonResponse({"error": "Interview information not found for the given application_id."}, status=400)
        
        data = json.loads(request.body)
        user_message = data.get("User_Message", "")

        conversation_key = "Interview_messages"

        interview_doc = interview_collection.find_one({"Application_ID": application_id})
        if interview_doc:
            messages = interview_doc.get(conversation_key, [])

        else:
            messages = [
                {
                    "role": "system", "content": f'''
                    You are a HR Bot for the company {interview_info.get("company")}.
                    You are interviewing a candidate for the job of {interview_info.get("job")}.
                    Job Description: {interview_info.get("job_description")}
                    Resume Summary of the Candidate: {interview_info.get("resume_summary")}

                    This is a real interview, begin it with a short introduction about yourself, the company and the job 
                    Keep the interview short, about 15 minuites.
                    The objective of the interview is to decide the compatibality of the candidate with the job.
                    Ask only one question at a time, proceed to ask the next question once the candidate responds. 
                    Your conversation should be short and concise.

                    The interview Begins now!
                    '''
                }
            ]
            # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature= 0, messages=messages)
            # system_message = response["choices"][0]["message"]
            # messages.append(system_message) 


        messages.append({"role": "user", "content": user_message})        
        
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature= 0, messages=messages)
        system_message = response["choices"][0]["message"]
        messages.append(system_message) 

        interview_collection.update_one(
            {"Application_ID": application_id},
            {
                "$set": {
                    conversation_key: messages,   
                }
            },
            upsert=True  # Create a new document if none exists for the given application_id
        )

        return JsonResponse({
            "conversation": messages
        })

def format_interview(application_id):
    # Retrieve the candidate information from hrms.interview
    interview = interview_collection.find_one({"Application_ID": application_id})

    if not interview:
        # Return an error response if interview is empty
        return {"error": "No Interview was conducted for the given application_id."}

    # Initialize an empty string to hold the formatted interview
    formatted_interview = ""

    # Variable to keep track of the last role for proper formatting
    last_role = None

    # Mapping dictionary to change roles from "User" to "Candidate" and "Assistant" to "Interviewer"
    role_mapping = {
        "user": "Candidate",
        "assistant": "Interviewer"
    }

    # Loop through the interview messages
    for message in interview['Interview_messages']:
        # Skip system messages
        if message['role'] == 'system':
            continue

        # Convert role from "User" to "Candidate" and "Assistant" to "Interviewer"
        role = role_mapping.get(message['role'], message['role'])

        # Check if the role of the current message is the same as the last role
        # If not, add the role name followed by a colon
        if role != last_role:
            formatted_interview += f"{role.title()}: "

        # Append the content of the message
        formatted_interview += f"{message['content'].strip()}\n\n"

        # Update the last_role with the current message role
        last_role = role

    return formatted_interview


@csrf_exempt
def evaluate_interview(request, application_id):
    if request.method == 'POST':
        
        formatted_interview = format_interview(application_id)

        interview_info = get_interview_info(application_id)
        if not interview_info:
            return JsonResponse({"error": "Interview information not found for the given application_id."}, status=400)
        
        resume_summary = interview_info.get("resume_summary")
        job_summary = interview_info.get("job_summary")

        result = get_interview_result(job_summary, resume_summary, formatted_interview)
        
        # Find the interview document based on the application_id
        interview_doc = interview_collection.find_one({"Application_ID": str(application_id)})

        if interview_doc:
            # Update the interview document with the interview result
            interview_collection.update_one(
                {"_id": interview_doc["_id"]},
                {"$set": {"interview_result": result}}
            )

            return JsonResponse(result)
        else:
            return JsonResponse({"error": "Interview document not found for the given application_id."}, status=400)
        

def get_interview_result(job_summary, resume_summary, formatted_interview):
    agent = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    temperature=0.0,
    messages=[
            {"role": "system", "content":'''
                You are an Interview Evaluation Bot

                **Instruction for Interview Evaluation Bot:**

                **Input:** "job_summary," "resume_summary," and "formatted_interview" fields.
                eg:
                    "job_summary": "Job summary containing details of the job",
                    "resume_summary": "Summary of the candidate's resume and relevant experience.",
                    "formatted_interview": "The transcript of the automated interview between the candidate and the HR bot."

                **Task:** Evaluate the interview transcript based on candidate responses and job relevancy.

                **Output JSON:** Include "interview_score," "proceed_to_next_round," "reason," "strengths," "areas_for_improvement," "additional_feedback," and "relevant_skills."

                **Evaluation Criteria:** Score candidate suitability for the job (0-100) based on responses.

                **Decision and Reasoning:** Set "proceed_to_next_round" based on score. Provide concise reasons.

                **Feedback:** List strengths, areas for improvement, and additional feedback.

                **Skill Relevance:** Extract relevant skills mentioned during the interview.

                ** For ease of communication and clarity, your output must strictly adhere to the stringified JSON Object format:**
                {
                    "interview_score": X,
                    "proceed_to_next_round": true/false,
                    "reason": "Concise reason for proceeding or not.",
                    "strengths": ["List of candidate's strengths."],
                    "areas_for_improvement": ["List of areas for improvement."],
                    "additional_feedback": "Any other relevant feedback.",
                    "relevant_skills": ["List of relevant skills."]
                }
                '''
             },
        
        
            {"role": "user", "content": f'''
                    "job_summary": {job_summary},
                    "resume_summary": {resume_summary},
                    "formatted_interview": {formatted_interview}
            '''},
        ]
    )

    result = json.loads(agent.choices[0].message.content)

    print(result)

    return result


@csrf_exempt
def post_job_preview(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job = data.get("Job", "")
            about_company = data.get("About_Company", "")
            job_description = data.get("Job_Description", "")

            enhanced_job_posting:str = improve_job_posting(job, about_company, job_description)
            print(enhanced_job_posting)
            dict = json.loads(enhanced_job_posting)
            return JsonResponse(dict, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@csrf_exempt
def post_job(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            inserted_document = jobs_collection.insert_one(data)
            job_id = str(inserted_document.inserted_id) 

            response_data = {
                'message': 'Job Posted successfully.',
                'jobID': job_id  
            }

            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

def get_jobs(request):
    if request.method == 'GET':
        jobs = list(jobs_collection.find({}))
        processed_jobs = []
        for job in jobs:
            job_id = str(job["_id"])
            processed_job = {
                "Job_ID": job_id,
                "Job": job["Job"],
                "Job_Description": job["Job_Description"],
                "About_Company": job["About_Company"],
                "Job_Summary": job["Job_Summary"],
            }
            processed_jobs.append(processed_job)

        jobs_json = json.dumps(processed_jobs, default=json_util.default)
        return HttpResponse(jobs_json, content_type='application/json')
    else:
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

@csrf_exempt
def get_suggestions(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            job_id = data.get("Job_ID", "")
            resume = data.get("Resume", "")

            job_document = jobs_collection.find_one({"_id": ObjectId(job_id)})
            if job_document:
                job = job_document.get("Job", "")
                job_description = job_document.get("Job_Description", "")
            else:
                return JsonResponse({'error': 'Invalid Job_ID.'}, status=404)

            insights = get_insights(job, job_description, resume)
            insights_dict = json.loads(insights)

            return JsonResponse(insights_dict, safe=False)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@csrf_exempt
def post_application(request):
    if request.method == 'POST':
        try:
            application = json.loads(request.body)
            
            job_id = application.get('Job_ID')
            resume_summary = application.get('Resume_Summary')
            screening_questions = application.get('Screening_Questions')
            answers = application.get('Answers')
            email = application.get('Email')
            
            if screening_questions and answers and len(screening_questions) == len(answers):
                question_answer_pairs = []
                
                for i, question in enumerate(screening_questions):
                    answer = answers[i]
                    question_answer_pairs.append(f"Q{i+1}. {question}\nA{i+1}. {answer}\n")
                
                result_string = "\n".join(question_answer_pairs)
                
                application_data = {
                    'Job_ID': job_id,
                    'Resume_Summary': resume_summary,
                    'Question_Answer_Pairs': result_string,
                }
        
            inserted_application = applications_collection.insert_one(application)
            application_id = str(inserted_application.inserted_id)

            # Check if a file is uploaded
            if 'Resume_File' in request.FILES:
                resume_file = request.FILES['Resume_File']

                # Get the file extension
                file_extension = resume_file.name.split('.')[-1].lower()

                # Save the file locally
                file_name = f"{application_id}_resume.{file_extension}"
                file_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Directory where the file should be saved
                os.makedirs(file_dir, exist_ok=True)  # Ensure the directory exists
                file_path = os.path.join(file_dir, file_name)  # Full file path including the filename
                with open(file_path, 'wb') as file:
                    for chunk in resume_file.chunks():
                        file.write(chunk)


            result_dict = evaluate_resume(application_data)
            result_dict = {'Application_ID': application_id, 'Email': email,  **result_dict}

            result = processed_applications_collection.insert_one(result_dict)
            result_id = str(result.inserted_id)
            
            return JsonResponse({"Application_ID": application_id, "Result_ID": result_id}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    

@csrf_exempt
def delete_job(request, job_id):
    if request.method == 'DELETE':
        try:
            # Convert the provided job_id to a valid ObjectId
            from bson import ObjectId
            job_id = ObjectId(job_id)
            
            # Check if the job with the given job_id exists in the collection
            job = jobs_collection.find_one({"_id": job_id})
            if job is None:
                return JsonResponse({'error': 'Job not found.'}, status=404)

            # Delete the job from the collection
            jobs_collection.delete_one({"_id": job_id})
            return JsonResponse({'message': 'Job deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only DELETE requests are allowed.'}, status=405)


@csrf_exempt
def edit_job(request, job_id):
    if request.method == 'PUT':
        try:
            # Convert the provided job_id to a valid ObjectId
            from bson import ObjectId
            job_id = ObjectId(job_id)

            # Check if the job with the given job_id exists in the collection
            job = jobs_collection.find_one({"_id": job_id})
            if job is None:
                return JsonResponse({'error': 'Job not found.'}, status=404)

            # Get the updated data from the request body
            data = json.loads(request.body)

            # Update the job in the collection
            jobs_collection.update_one({"_id": job_id}, {"$set": data})
            return JsonResponse({'message': 'Job updated successfully.'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed.'}, status=405)

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
@csrf_exempt
def send_emails(request):
    if request.method == 'POST':
        try:
            K = int(request.GET.get('K', 5)) 
            top_applications = list(processed_applications_collection.find().sort("Final_Score", -1).limit(K))

            processed_top_applications = []

            for application in top_applications:
                application_id = application["Application_ID"]
                candidate_name = application["Candidate_Name"]
                recipient_email = application["Email"]
                sender_email = smtp_email

                message = f'''Dear {candidate_name}, Congratulations! We are impressed with your application, Link: http://127.0.0.1:8000/jobs/get_application/{application_id}/ and would like to invite you for an interview. Interview Link: http://localhost:4200/interview?id={application_id} Please appear for the interview within 72 hrs of receiving this email.
                '''
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient_email
                msg['Subject'] = "IMPORTANT: Interview Invite"
                msg.attach(MIMEText(message, 'plain'))
                smtp_server = 'localhost'  # Change this to your local SMTP server address
                smtp_port = 25  # Change this to your SMTP server port

                try:
                    smtp = smtplib.SMTP(smtp_server, smtp_port)
                    smtp.sendmail(sender_email, recipient_email, msg.as_string())
                    smtp.quit()

                    processed_application = {
                        "Application_ID": application_id,
                        "Candidate_Name": candidate_name,
                        "Email": recipient_email,
                        "Email_msg": message,
                        "Email_sent_status": "Sent"
                    }
                    processed_top_applications.append(processed_application)

                    print(f"Email sent successfully to {recipient_email}")
                except Exception as e:
                    processed_application = {
                        "Application_ID": application_id,
                        "Candidate_Name": candidate_name,
                        "Email": recipient_email,
                        "Email_msg": message,
                        "Email_sent_status": "Error"
                    }
                    processed_top_applications.append(processed_application)

                    print(f"Error sending email to {recipient_email}: {e}")

            applications_json = json.dumps(processed_top_applications, default=json_util.default)
            return HttpResponse(applications_json, content_type='application/json')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def get_all_applications(request):
    if request.method == 'GET':
        try:
            applications_collection = db["applications"]
            processed_applications_collection = db["processed_applications"]

            # Get all applications from the 'applications' collection
            all_applications = list(applications_collection.find())

            # Initialize a list to store the combined application and result data
            all_applications_with_results = []

            for application in all_applications:
                application_id = str(application["_id"])

                # Find the corresponding processed application from 'processed_applications' collection
                processed_application = processed_applications_collection.find_one(
                    {"Application_ID": application_id}
                )

                if processed_application:
                    # Merge the application and processed application data
                    merged_data = {
                        "Application_ID": application_id,
                        "Job_ID": application["Job_ID"],
                        "Candidate_Name": application["Name"],
                        "Email": application["Email"],
                        "Contact": application["Contact"],
                        "Resume": application["Resume"],
                        "Improvements": application["Improvements"],
                        "Screening_Questions": application["Screening_Questions"],
                        "Answers": application["Answers"],
                        "Resume_Score": processed_application["Resume_Score"],
                        "Candidate_Compatibility_with_Job": processed_application["Candidate_Compatibility_with_Job"],
                        "Overall_Candidate_Rating_Irrespective_of_Job_Description": processed_application["Overall_Candidate_Rating_Irrespective_of_Job_Description"],
                        "Qualities_Matching_with_Job": processed_application["Qualities_Matching_with_Job"],
                        "Five_Impressive_Qualities_Irrespective_of_Job_Description": processed_application["Five_Impressive_Qualities_Irrespective_of_Job_Description"],
                        "Five_Weaknesses": processed_application["Five_Weaknesses"],
                        "Final_Thoughts": processed_application["Final_Thoughts"],
                        "Final_Score": processed_application["Final_Score"],
                    }

                    # Append the merged data to the list
                    all_applications_with_results.append(merged_data)

            applications_json = json.dumps(all_applications_with_results, default=json_util.default)
            return HttpResponse(applications_json, content_type='application/json')

        except Exception as e:
            # Handle any exceptions that might occur during the process
            return HttpResponse(json.dumps({"error": str(e)}), content_type='application/json', status=500)


def get_applications_for_job(request, job_id):
    if request.method == 'GET':
        try:
            applications_collection = db["applications"]
            processed_applications_collection = db["processed_applications"]

            # Get all applications for the specified job_id from the 'applications' collection
            job_applications = list(applications_collection.find({"Job_ID": job_id}))

            # Initialize a list to store the combined application and result data
            job_applications_with_results = []

            for application in job_applications:
                application_id = str(application["_id"])

                # Find the corresponding processed application from 'processed_applications' collection
                processed_application = processed_applications_collection.find_one(
                    {"Application_ID": application_id}
                )

                if processed_application:
                    # Merge the application and processed application data
                    merged_data = {
                        "Application_ID": application_id,
                        "Job_ID": application["Job_ID"],
                        "Candidate_Name": application["Name"],
                        "Email": application["Email"],
                        "Contact": application["Contact"],
                        "Resume": application["Resume"],
                        "Improvements": application["Improvements"],
                        "Screening_Questions": application["Screening_Questions"],
                        "Answers": application["Answers"],
                        "Resume_Score": processed_application["Resume_Score"],
                        "Candidate_Compatibility_with_Job": processed_application["Candidate_Compatibility_with_Job"],
                        "Overall_Candidate_Rating_Irrespective_of_Job_Description": processed_application["Overall_Candidate_Rating_Irrespective_of_Job_Description"],
                        "Qualities_Matching_with_Job": processed_application["Qualities_Matching_with_Job"],
                        "Five_Impressive_Qualities_Irrespective_of_Job_Description": processed_application["Five_Impressive_Qualities_Irrespective_of_Job_Description"],
                        "Five_Weaknesses": processed_application["Five_Weaknesses"],
                        "Final_Thoughts": processed_application["Final_Thoughts"],
                        "Final_Score": processed_application["Final_Score"],
                    }

                    # Append the merged data to the list
                    job_applications_with_results.append(merged_data)

            applications_json = json.dumps(job_applications_with_results, default=json_util.default)
            return HttpResponse(applications_json, content_type='application/json')

        except Exception as e:
            # Handle any exceptions that might occur during the process
            return HttpResponse(json.dumps({"error": str(e)}), content_type='application/json', status=500)


def get_application(request, application_id):
    if request.method == 'GET':
        try:
            applications_collection = db["applications"]

            # Convert the application_id string to ObjectId
            application_id = ObjectId(application_id)

            # Find the application with the specified _id
            application = applications_collection.find_one({"_id": application_id})

            if application:
                # Convert ObjectId to string before serializing
                application["_id"] = str(application["_id"])
                application_json = json.dumps(application)
                return HttpResponse(application_json, content_type='application/json')
            else:
                return HttpResponse(json.dumps({"error": "Application not found"}), content_type='application/json', status=404)

        except Exception as e:
            # Handle any exceptions that might occur during the process
            return HttpResponse(json.dumps({"error": str(e)}), content_type='application/json', status=500)
        


def get_top_applications(request):
    if request.method == 'GET':
        try:
            K = int(request.GET.get('K', 5))  # Default to 5 if K is not provided in the request
            processed_applications_collection = db["processed_applications"]
            top_applications = list(processed_applications_collection.find().sort("Final_Score", -1).limit(K))

            # Process the top applications if needed (as you did in the original view)
            processed_top_applications = []
            for application in top_applications:
                application_id = str(application["_id"])
                processed_application = {
                    "Application_ID": application_id,
                    "Candidate_Name": application["Candidate_Name"],
                    "Final_Score": application["Final_Score"],
                    "Summary": application["Final_Thoughts"]
                    # Add more fields you want to include in the processed data
                }
                processed_top_applications.append(processed_application)

            applications_json = json.dumps(processed_top_applications, default=json_util.default)
            return HttpResponse(applications_json, content_type='application/json')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)
    

def improve_job_posting(job, about_company, job_description):
    agent = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    temperature=0.0,
    messages=[
            {"role": "system", "content": '''
                Create a compelling and concise job description in JSON format using the given input. 

                ### Input:
                {
                    "Job": "[Original Job Title]",
                    "Job_Description": "[Original Job Description]",
                    "About_Company": "[About the Company]"
                }

                For ease of communication and clarity, your output must strictly adhere to the stringified JSON Object format:
                
                ### Output:
                {
                    "Job": "[New Job Title]",
                    "Job_Description": "[Improved and optimized Job Description]",
                    "About_Company": "[New About Company]",
                    "Job_Summary": "[Concise summary that covers Everything about the Job with some details about company]",
                    "Changes_Made": "[Summary of changes/improvements in the new Job Description and its benefits]"
                }
             '''},
        
            {"role": "user", "content": f'''
             ###Input:

             ###Job: {job}

             ###Job_Description: {job_description}
             
             ###About_Company: {about_company}
            
             ###Result:
            '''},
        ]
    )

    return agent.choices[0].message.content


def get_insights(job, job_description, candidate_resume):
    agent = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    temperature=0.0,
    messages=[
            {"role": "system", "content": '''
                As an exceptional HR professional, your expertise lies in meticulously evaluating candidates' resumes and assessing their compatibility with job descriptions by developing tailored screeing questions based on the provided Job Description and candidate's Resume. Your process entails a thorough examination of the candidates' resumes, followed by crafting an exhaustive and detailed summary, leaving no crucial information overlooked.

                Next, you diligently compare the resume summary with the job description and provide a maximum of five crucial pieces of feedback for improvement, if necessary. Should the resume meet the required standards, it is essential to acknowledge the candidate's commendable efforts in the improvements section.

                Your ability to identify and highlight weaknesses in resumes allows you to offer valuable feedback directly to the candidates. Moreover, you excel at developing precisely five screening questions for each candidate, meticulously aligning them with the job description and the candidate's resume. These screening questions serve as invaluable tools for assessing the candidate's competencies in line with the job requirements.

                Provide improvements directly to the candidate eg. "Your resume doesn't highlight any specific experience or knowledge in [Some requirement for job], which is a requirement for this position."

                For ease of communication and clarity, your output must strictly adhere to the stringified JSON Object format:

                ###Result:
                {
                    "Resume_Summary": "[An extremely detailed, comprehensive, complete, and exhaustive summary/description of the candidate's resume]",
                    "Improvements": ["Improvement 1", "Improvement 2", "Improvement 3", "Improvement 4", "Improvement 5"],
                    "Screening_Questions": ["Question 1", "Question 2", "Question 3", "Question 4", "Question 5"]
                }

                Adhering to this standardized format ensures a clear and consistent approach when delivering your evaluations and feedback to both the candidates and the hiring team. Your exceptional skills in this area undoubtedly contribute significantly to the company's hiring process, ultimately leading to the discovery of the best-suited candidates for various positions.
                            
             '''},
        
            {"role": "user", "content": f'''
             
             ###Job: {job}

             ###Job Description: {job_description}
             
             ###Resume: {candidate_resume}
            
             ###Result:
            '''},
        ]
    )
    return agent.choices[0].message.content


def evaluate_resume(application):
    job_id = application.get("Job_ID")
    resume_summary = application.get("Resume_Summary")
    question_answer_pairs = application.get("Question_Answer_Pairs")

    print(question_answer_pairs)

    job_document = jobs_collection.find_one({"_id": ObjectId(job_id)})
    if job_document:
        job = job_document.get("Job", "")
        job_description = job_document.get("Job_Description", "")
    else:
        return JsonResponse({'error': 'Invalid Job_ID.'}, status=404)

    agent = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    temperature=0.0,
    messages=[
            {"role": "system", "content":'''As an exceptional HR professional, you possess expertise in evaluating candidates' resumes and accurately assessing their compatibility with job descriptions. Moreover, you are highly efficient in ranking resumes on a scale of 0 to 100, ensuring a thorough and effective candidate assessment process. You will also be provided few screening questions and corresponding answers by candidate, which will help you evalate candidate.

            The user will provide input in the following format:
            ###Job: [Contains the job title]

            ###Job_Description: [Contains the job description and information about the company.]

            ###Resume_Summary: [Contains a brief summary of the candidate's resume]
             
            ###QnA_pairs: [Contains Screening Questions and Corresponding Answers from candidate]

            **Your output must strictly adhere to the stringified JSON Object format:**

            ###Result:
            {
                "Candidate_Name": "string - Name of the candidate to whom the resume belongs",
                "Resume_Score": "int - Score on a scale of 0 to 100, reflecting the quality and suitability of the candidate's resume",
                "Candidate_Compatibility_with_Job": "int - Score on a scale of 0 to 100, indicating the candidate's compatibility with the job",
                "Overall_Candidate_Rating_Irrespective_of_Job_Description": "int - Score on a scale of 0 to 100, representing the candidate's overall qualities and potential irrespective of the job description",
                "Qualities_Matching_with_Job": ["list - 0 to 5 qualities that match the job description, each described in one line"],
                "Five_Impressive_Qualities_Irrespective_of_Job_Description": ["list - 0 to 5 impressive qualities of the candidate that stand out regardless of the job description, each described in one line"],
                "Five_Weaknesses": ["list - 0 to 5 weaknesses of the candidate, each described in one line"],
                "Final_Thoughts": ["list - Overall summary of the candidate in brief, highlighting key points from the evaluation"]
                "Final_Score":  "int - Final Score on a scale of 0 to 100" 
            }
            '''},
        
        
            {"role": "user", "content": f'''
             
             ###Job: {job}
             
             ###Job_Description: {job_description}
             
             ###Resume_Summary: {resume_summary}

             ###QnA_Pairs: {question_answer_pairs}
            
             ###Result:
            '''},
        ]
    )

    result = json.loads(agent.choices[0].message.content)
    return convert_object_id_to_string(result)


def convert_object_id_to_string(obj):
    if isinstance(obj, list):
        return [convert_object_id_to_string(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_object_id_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj
    

def send_interview_email(sender_email, sender_password, recipient_email, candidate_name, summary):
    try:
        # Set up the SMTP server
        smtp_server = "smtp.example.com"  # Replace with your SMTP server address
        smtp_port = 587  # Replace with the appropriate SMTP port
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure, encrypted one
        server.login(sender_email, sender_password)

        # Create the email message
        subject = "Interview Invitation"
        message = f"Dear {candidate_name},\n\nCongratulations! We are impressed with your application and would like to invite you for an interview.\n\nSummary: {summary}\n\nPlease let us know your availability for the interview.\n\nBest regards,\nYour Company Name"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, "plain"))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the SMTP server connection
        server.quit()
        print(f"Interview email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending interview email to {recipient_email}: {str(e)}")


def get_all_interviews(request):
    if request.method == 'GET':
        try:

            # Fetch all documents from the collection
            all_documents_from_interview_collection = list(interview_collection.find({}))

            # Convert documents to JSON
            applications_json = json.dumps(all_documents_from_interview_collection, default=json_util.default)

            return HttpResponse(applications_json, content_type='application/json')

        except Exception as e:
            # Handle any exceptions that might occur during the process
            return HttpResponse(json.dumps({"error": str(e)}), content_type='application/json', status=500)

from bson import ObjectId

def get_interviews_for_job(request, job_id):
    if request.method == 'GET':
        try:
            print("job_id: ", job_id)
            # Find the applications for the specified job_id
            applications_cursor = applications_collection.find({"Job_ID": job_id})
            applications = list(applications_cursor)
            print("applications: ", applications)
            
            application_ids = [str(app['_id']) for app in applications]  # Convert ObjectId to string
            print("application_ids", application_ids)
            
            # Fetch interviews for the specified application IDs
            interviews_for_job = list(interview_collection.find({"Application_ID": {"$in": application_ids}}))
            print("interviews: ", interviews_for_job)
            
            # Build a response JSON with applicant details and interview data
            response_data = []
            for interview in interviews_for_job:
                application_id = interview["Application_ID"]
                applicant_details = next((app for app in applications if str(app['_id']) == application_id), None)
                if applicant_details:
                    interview["Applicant_Details"] = {
                        "Name": applicant_details["Name"],
                        "Email": applicant_details["Email"],
                        "Contact": applicant_details["Contact"]
                    }
                response_data.append(interview)
            
            # Convert response data to JSON
            response_json = json.dumps(response_data, default=json_util.default)

            return HttpResponse(response_json, content_type='application/json')

        except Exception as e:
            # Handle any exceptions that might occur during the process
            return HttpResponse(json.dumps({"error": str(e)}), content_type='application/json', status=500)
