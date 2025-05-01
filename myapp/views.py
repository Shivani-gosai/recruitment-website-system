from django.shortcuts import render,redirect

# Create your views here.
from .forms import LoginForm
from .models import Login,Organization,Post,Followers,Comments
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#Auth from
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import (MemberForm, MemberEducationForm, MemberSkillsForm,
                    MemberExperienceForm, MemberLanguageForm, 
                    MemberLinkForm, SummaryForm)
from .models import (Member, MemberEducation, MemberSkills, MemberExperience,
                     MemberLanguage, MemberLink, Summary)

#auth form
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from .forms import MemberForm,Login,LoginForm,Agency,AgencyForm
from .forms import MemberEducationForm, MemberSkillsForm, MemberExperienceForm
from .forms import Member,OrganizationForm,PostForm
from django.http import JsonResponse
from .models import City
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

# Load Encryption Key
from django.contrib.auth.hashers import check_password
from cryptography.fernet import Fernet
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError


# cipher = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())

# @csrf_exempt
# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']

#             user = None
#             user_type = None

#             # ✅ Check for Job Seeker (Member)
#             try:
#                 user = Member.objects.get(eemail=email)
#                 user_type = "jobseeker"
#             except Member.DoesNotExist:
#                 pass

#             # ✅ Check for Agency
#             if not user:
#                 try:
#                     user = Agency.objects.get(email_address=email)
#                     user_type = "agency"
#                 except Agency.DoesNotExist:
#                     pass

#             # ✅ Check for Organization (Business)
#             if not user:
#                 try:
#                     user = Organization.objects.get(stremail=email)
#                     user_type = "business"
#                 except Organization.DoesNotExist:
#                     pass

#             # ✅ Validate Password and Store Login Data
#             if user:
#                 try:
#                     decrypted_password = cipher.decrypt(user.password.encode()).decode()
#                     print(f"Decrypted Password: {decrypted_password}")  # Debugging

#                     if decrypted_password == password:
#                         # ✅ Store login session
#                         login_entry, created = Login.objects.update_or_create(
#                             stremail=email,
#                             user_type=user_type,
#                             defaults={"password": user.password}  # Update password if changed
#                         )

#                         request.session['login_id'] = login_entry.id
#                         request.session['stremail'] = login_entry.stremail
#                         request.session['user_type'] = login_entry.user_type
#                         request.session['is_logged_in'] = True  # ✅ User is logged in

#                         messages.success(request, f"{user_type.capitalize()} login successful!")

#                         print(f"Session Data: {request.session.items()}")  # Debugging session storage
#                         print(f"Redirecting to: {reverse('new_profile_view')}")  # Debugging redirect

#                         return redirect(reverse("new_profile_view"))  # ✅ Redirect to Profile Page
#                     else:
#                         messages.error(request, "Invalid email or password.")
#                 except Exception as e:
#                     print(f"Decryption Error: {e}")  # Debugging
#                     messages.error(request, "Error decrypting password.")
#             else:
#                 messages.error(request, "User not found. Please register.")
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.conf import settings
from cryptography.fernet import Fernet
from .models import Member, Agency, Organization, Login
from .forms import LoginForm

cipher = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Member, Organization, Agency, Login
from .forms import LoginForm
from cryptography.fernet import Fernet
from django.conf import settings

from .models import Job   # Make sure you import your Job model

from .models import Job, Member  # Make sure you import Member model too

def firstpage(request):
    recent_jobs = Job.objects.all().order_by('-id')[:4]  # Fetch 4 recent jobs
    recent_members = Member.objects.all().order_by('-id')[:5]  # Fetch 5 recent members
    return render(request, 'index.html', {
        'recent_jobs': recent_jobs,
        'recent_members': recent_members,
    })


cipher = Fernet(settings.SECRET_ENCRYPTION_KEY.encode())

@csrf_exempt
def login(request):
    """
    Authenticates users as Jobseeker, Agency, or Business.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = None
            user_type = None

            # ✅ Check for Jobseeker
            try:
                user = Member.objects.filter(eemail=email).first()
                user_type = "jobseeker"
            except Member.DoesNotExist:
                pass
            except Member.MultipleObjectsReturned:
                #messages.error(request, "Multiple jobseeker accounts found with this email.")
                return redirect("login")

            # ✅ Check for Agency
            if not user:
                try:
                    user = Agency.objects.get(email_address=email)
                    user_type = "agency"
                except Agency.DoesNotExist:
                    pass
                except Agency.MultipleObjectsReturned:
                    #messages.error(request, "Multiple agency accounts found with this email.")
                    return redirect("login")

            # ✅ Check for Organization
            if not user:
                try:
                    user = Organization.objects.get(stremail=email)
                    user_type = "business"
                except Organization.DoesNotExist:
                    pass
                except Organization.MultipleObjectsReturned:
                    #messages.error(request, "Multiple business accounts found with this email.")
                    return redirect("login")

            # ✅ Validate password
            if user:
                try:
                    decrypted_password = cipher.decrypt(user.password.encode()).decode()

                    if decrypted_password == password:
                        # ✅ Create or update Login record
                        login_entry, _ = Login.objects.update_or_create(
                            stremail=email,
                            defaults={"password": user.password, "user_type": user_type}
                        )

                        # ✅ Link login to Agency or Organization if needed
                        if user_type == "agency" and user.login != login_entry:
                            user.login = login_entry
                            user.save()
                        elif user_type == "business" and user.login != login_entry:
                            user.login = login_entry
                            user.save()

                        # ✅ Set session
                        request.session['login_id'] = login_entry.id
                        request.session['stremail'] = login_entry.stremail
                        request.session['user_type'] = login_entry.user_type
                        request.session['is_logged_in'] = True

                        #messages.success(request, f"{user_type.capitalize()} login successful!")

                        # ✅ Redirect accordingly
                        if user_type == "jobseeker":
                            return redirect("new_profile_view")
                        elif user_type == "business":
                            return redirect("cmphome", user.id)
                        elif user_type == "agency":
                            return redirect(reverse('agency_homepage'))
                    else:
                        #messages.error(request, "Invalid email or password.")
                        pass
                except Exception as e:
                    print("❌ Decryption error:", e)
                    #messages.error(request, "Error decrypting password.")
            else:
                #messages.error(request, "User not found. Please register.")
                pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})





def dashboard(request):
    """
    Organization Dashboard view (Protected Route).
    - Ensures only logged-in organizations can access.
    """
    if 'organization_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('/login') 

    organization = Organization.objects.get(id=request.session['organization_id'])
    return render(request, 'dashboard.html', {'organization': organization})




'''from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Organization

def cmphome(request):
    """Handles displaying and updating the company introduction and overview"""
    email = request.session.get("stremail")

    if not email:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # AJAX request check
            return JsonResponse({"success": False, "message": "Session expired. Please log in again."})
        messages.error(request, "Session expired. Please log in again.")
        return redirect("login")

    try:
        organization = Organization.objects.get(stremail=email)
    except Organization.DoesNotExist:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "message": "Organization not found."})
        messages.error(request, "Organization not found.")
        return redirect("some_other_view")

    if request.method == "POST":
        intro = request.POST.get("companyIntroduction", "").strip()
        overview = request.POST.get("companyOverview", "").strip()
        
        organization.intro = intro
        organization.overview = overview
        organization.save()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Company information updated successfully."})
        
        messages.success(request, "Company information updated successfully.")
        return redirect("cmphome")

    return render(request, "cmphome.html", {"organization": organization})



import json
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Organization

def cmpabout(request):
    email = request.session.get("stremail")
    if not email:
        messages.error(request, "Session expired. Please log in again.")
        return redirect("login")

    try:
        organization = Organization.objects.get(stremail=email)
        organization_values = json.loads(organization.values) if organization.values else []  # Convert JSON string to list
    except Organization.DoesNotExist:
        messages.error(request, "Organization not found.")
        return redirect("homepage")

    return render(request, "cmpabout.html", {"organization": organization, "values_list": organization_values})'''





# def cmphome(request):
#     user_email = request.session.get("stremail")
    
#     # Debugging: Check session email
#     if not user_email:
#         print("❌ No session email found!")
#         return redirect("login")  # Redirect if session is missing

#     print(f"✅ Session Email: {user_email}")  # Debugging

#     # Get organization based on email
#     organization = Organization.objects.filter(stremail=user_email).first()

#     print(f"🔍 Organization: {organization}")  # Debugging

#     return render(request, "cmphome.html", {"organization": organization})

# In views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Only if needed (for testing or if CSRF fails)
from django.shortcuts import render, get_object_or_404
from .models import Organization, Post, Followers, Login

def cmphome(request, org_id):
    # ✅ Get the organization object first
    organization = get_object_or_404(Organization, id=org_id)

    if request.method == "POST":
        intro = request.POST.get("companyIntroduction")
        overview = request.POST.get("companyOverview")

        if intro is not None:
            organization.intro = intro
        if overview is not None:
            organization.overview = overview

        organization.save()

        return JsonResponse({'success': True})

    # ✅ Get posts
    posts = Post.objects.filter(login__stremail=organization.stremail).order_by('-id')

    jobs = Job.objects.filter(organization=organization).order_by('-id')[:3]  # latest 3 jobs

    # ✅ Get follower count
    follower_count = Followers.objects.filter(followid=org_id).count()

    # ✅ Check if current user follows this organization
    is_following = False
    user_email = request.session.get("stremail")
    login = Login.objects.filter(stremail=user_email).first()
    if login:
        is_following = Followers.objects.filter(followid=org_id, login=login).exists()

    # ✅ Pass to template
    context = {
        'organization': organization,
        'posts': posts,
        'follower_count': follower_count,
        'is_following': is_following,
        'jobs': jobs,  # pass jobs to template
    }

    return render(request, 'cmphome.html', context)


# In your views.py
def some_view_that_redirects_to_cmphome(request):
    # Assuming you already have the organization object
    organization = Organization.objects.get(stremail=request.session.get('stremail'))  # Fetch organization
    return redirect('cmphome', org_id=organization.id)  # Pass the org_id





# def cmpabout(request):
#     user_email = request.session.get("stremail")

#     if not user_email:
#         return redirect("login")  # Redirect to login if session is missing

#     # Get organization and agency based on email
#     organization = Organization.objects.filter(stremail=user_email).first()

#     print(f"Session Email: {user_email}")  # Debugging
#     print(f"Organization: {organization}")  # Debugging

#     return render(request, "cmpabout.html", {"organization": organization})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Followers, Organization, Login

def cmpabout(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)

    if request.method == "POST":
        organization.mission = request.POST.get("mission", "")
        organization.vision = request.POST.get("vision", "")
        organization.values = request.POST.get("values", "")
        organization.save()
        return redirect("cmpabout", org_id=org_id)

    follower_count = Followers.objects.filter(followid=org_id).count()

    user_email = request.session.get("stremail")
    login = Login.objects.filter(stremail=user_email).first()
    is_following = Followers.objects.filter(followid=org_id, login=login).exists() if login else False

    # Decode values safely
    values_list = []
    if organization.values:
        try:
            values_list = json.loads(organization.values)
        except json.JSONDecodeError:
            pass

    return render(request, "cmpabout.html", {
        "organization": organization,
        "follower_count": follower_count,
        "is_following": is_following,
        "values_list": values_list,
    })

@csrf_exempt
@require_POST
def update_org_details(request, org_id):
    try:
        organization = Organization.objects.get(id=org_id)
        data = json.loads(request.body)

        mission = data.get("mission")
        vision = data.get("vision")
        values = data.get("values")

        if mission is not None:
            organization.mission = mission
        if vision is not None:
            organization.vision = vision
        if values is not None:
            organization.values = json.dumps(values)  # save as JSON string

        organization.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



from .models import Followers, Job, Login, Organization
from django.shortcuts import render
from django.http import HttpResponse

def cmpjob(request, org_id):
    organization = Organization.objects.filter(id=org_id).first()
    if not organization:
        return HttpResponse("❌ Organization not found.", status=404)

    query = request.GET.get('q', '')
    # ✅ Only fetch jobs posted directly by the organization (exclude agency reposts)
    jobs = Job.objects.filter(organization=organization, agency__isnull=True)

    if query:
        jobs = jobs.filter(position__icontains=query)

    # ✅ Follow status and follower count
    is_following = False
    follower_count = Followers.objects.filter(followid=org_id).count()

    user_email = request.session.get("stremail")
    if user_email:
        login = Login.objects.filter(stremail=user_email).first()
        if login and Followers.objects.filter(followid=org_id, login=login).exists():
            is_following = True
        
    job_count = jobs.count()  # ✅ use filtered jobs here for accurate count
    job = jobs.first()

    return render(request, "cmpjob.html", {
        "organization": organization,
        "jobs": jobs,
        "is_following": is_following,
        "follower_count": follower_count,
        'job_count': job_count,
        "job": job,
    })


#delete particular job
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Job, Organization

def delete_job(request, org_id, job_id):
    # Ensure the organization exists
    organization = get_object_or_404(Organization, id=org_id)

    # Get the job belonging to that organization or posted by that organization
    job = get_object_or_404(Job, id=job_id)

    # Ensure the job is either posted by the org or reposted by agency
    if job.organization == organization or job.organization.agency == organization.agency:
        job.delete()
        messages.success(request, "✅ Job deleted successfully.")
    else:
        messages.error(request, "❌ You are not authorized to delete this job.")

    return redirect('cmpjob', org_id=org_id)







from django.shortcuts import render
from django.db.models import Q
from myapp.models import Job, City, Member

def job_card(request):
    query = request.GET.get('q', '').strip()
    city_id = request.GET.get('city', '').strip()
    experience = request.GET.get('experience', '').strip()
    max_salary = request.GET.get('salary', '').strip()
    selected_schedules = request.GET.getlist('schedule')

    jobs = Job.objects.select_related('organization', 'city').all()
    cities = City.objects.all()

    # 🔐 Get current logged-in member
    member = None
    if 'login_id' in request.session:
        try:
            member = Member.objects.get(login_id=request.session['login_id'])
        except Member.DoesNotExist:
            member = None

    # 🔍 Search
    if query:
        jobs = jobs.filter(
            Q(position__icontains=query) |
            Q(organization__cmpname__icontains=query)
        )

    # 📍 City filter
    if city_id:
        jobs = jobs.filter(city__id=city_id)

    # 📚 Experience filter
    if experience:
        jobs = jobs.filter(requiredexperience__icontains=experience)

    # 🗓️ Working schedule (e.g., Full Time, Internship)
    if selected_schedules:
        jobs = jobs.filter(jobtype__in=selected_schedules)

    # 💰 Salary filter (convert to list last)
    if max_salary:
        try:
            max_val = int(max_salary)
            min_val = 1200
            jobs = jobs.filter(salary__regex=r'^\d+$')  # Filter numeric salary strings
            jobs = [job for job in jobs if min_val <= int(job.salary) <= max_val]
        except ValueError:
            pass

    return render(request, 'job_card.html', {
        'jobs': jobs,
        'cities': cities,
        'member': member,
        'selected_city': city_id,
        'selected_experience': experience,
        'search_query': query,
        'selected_salary': max_salary,
        'selected_schedules': selected_schedules,
    })

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import date
from .models import Application, Job, Login, Member

@csrf_exempt
def apply_job(request, jobid):
    job = get_object_or_404(Job, id=jobid)

    if request.method == 'POST':
        login_id = request.session.get("login_id")
        user_type = request.session.get("user_type")

        # ✅ Must be logged in
        if not login_id or not user_type:
            messages.error(request, "You must be logged in to apply.")
            return redirect('/login')

        # ✅ Only jobseekers allowed
        if user_type != "jobseeker":
            messages.error(request, "Only jobseekers (members) can apply.")
            return redirect('/login')

        # ✅ Try to get the login object
        try:
            login = Login.objects.get(id=login_id)
        except Login.DoesNotExist:
            messages.error(request, "Login not found.")
            return redirect('/login')

        # ✅ Try to get the member
        try:
            member = Member.objects.get(login=login)
        except Member.DoesNotExist:
            # Check if there's a member with the same email
            member = Member.objects.filter(eemail=login.stremail).first()
            if member:
                member.login = login
                member.save()
            else:
                messages.error(request, "Jobseeker account not found.")
                return redirect('/login')

        # ✅ Get form data
        remarks = request.POST.get("remarks", "").strip()
        attachment = request.FILES.get("attachment")
        agree = request.POST.get("agree")

        if agree != "yes":
            messages.error(request, "You must confirm the details are correct.")
            return redirect(request.path)

        if not attachment:
            messages.error(request, "Please upload a file.")
            return redirect(request.path)

        if attachment.content_type != "application/pdf":
            messages.error(request, "Only PDF files are allowed.")
            return redirect(request.path)

        # ✅ Save application
        Application.objects.create(
            job=job,
            member=member,
            applydate=date.today(),
            status="Pending",
            remarks=remarks,
            attachment=attachment
        )

        messages.success(request, "Application submitted successfully!")
        return redirect('/applied_jobs')

    return render(request, 'apply_now.html', {'jobid': jobid})


from django.shortcuts import render
from .models import Application, Login, Member

def applied_jobs_view(request):
    # Get current user's email from session
    user_email = request.session.get("stremail")

    # Ensure session exists
    if not user_email:
        return render(request, "applied_jobs.html", {"applications": []})

    # Get login and member
    login = Login.objects.filter(stremail=user_email).first()
    member = Member.objects.filter(login=login).first()

    if not member:
        return render(request, "applied_jobs.html", {"applications": []})

    # Fetch applications with job and company details
    applications = Application.objects.select_related('job', 'job__organization').filter(member=member).order_by('-applydate')

    return render(request, "applied_jobs.html", {
        "applications": applications
    })

from django.shortcuts import render, get_object_or_404
from .models import Job, Login, Member, Organization, Agency

def view_details(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    user_type = None  # Default
    user_email = request.session.get('stremail')  # Get from session only once

    if user_email:
        login = Login.objects.filter(stremail=user_email).first()
        if login:
            if Member.objects.filter(login=login).exists():
                user_type = "member"
            elif Organization.objects.filter(login=login).exists():
                user_type = "organization"
            elif Agency.objects.filter(login=login).exists():
                user_type = "agency"

    return render(request, 'job_details.html', {
        'job': job,
        'user_type': user_type,
    })









from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Followers, Login

@csrf_exempt
def toggle_follow(request, org_id):
    if request.method == 'POST':
        try:
            user_email = request.session.get("stremail")
            login = Login.objects.filter(stremail=user_email).first()
            if not login:
                return JsonResponse({'success': False, 'error': 'User not logged in'})

            existing_follow = Followers.objects.filter(followid=org_id, login=login).first()

            if existing_follow:
                existing_follow.delete()
                return JsonResponse({'success': True, 'status': 'unfollowed'})
            else:
                Followers.objects.create(
                    followid=org_id,
                    login=login,
                    followdate=timezone.now().date()
                )
                return JsonResponse({'success': True, 'status': 'followed'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})






from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Job, Organization, City, Post

@csrf_exempt
def create_job(request, org_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    try:
        # ✅ Get organization instance
        organization = Organization.objects.filter(id=org_id).first()
        if not organization:
            return JsonResponse({'success': False, 'error': 'Organization not found'}, status=404)

        # ✅ Extract form data

        position = request.POST.get("position")
        noofvacancies = request.POST.get("noofvacancies")
        requiredqualification = request.POST.get("requiredqualification")
        requiredexperience = request.POST.get("requiredexperience")
        jobdescription = request.POST.get("jobdescription")
        jobtype = request.POST.get("jobtype")
        location = request.POST.get("location")
        lastdate = request.POST.get("lastdate")
        skillsrequired = request.POST.get("skillsrequired")
        salary = request.POST.get("salary")

        # ✅ Validate required fields
        if not all([position, jobdescription, jobtype, location, lastdate]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'})

        # ✅ City handling
        city_obj, _ = City.objects.get_or_create(cityname=location)

        # ✅ Get any existing post associated with the organization login
        login = organization.login
        post_instance = Post.objects.filter(login=login).first() if login else None

        # ✅ Create Job instance
        Job.objects.create(
            organization=organization,
            cmpname=organization.cmpname,
            position=position,
            noofvacancies=int(noofvacancies) if noofvacancies else 1,
            requiredqualification=requiredqualification,
            requiredexperience=requiredexperience,
            jobdescription=jobdescription,
            jobtype=jobtype,
            city=city_obj,
            applystartdate=timezone.now().date(),
            lastdate=lastdate,
            skillsrequired=skillsrequired,
            salary=salary,
            post=post_instance
        )

        return JsonResponse({'success': True})

    except Exception as e:
        print("❌ Error in create_job:", str(e))
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

from django.shortcuts import render, get_object_or_404
from .models import Job, Login, Member

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    user_email = request.session.get('stremail')
    login = Login.objects.filter(stremail=user_email).first() if user_email else None
    user_type = login.user_type if login else None

    return render(request, 'job_details.html', {
        'job': job,
        'user_type': user_type,
    })




'''@csrf_exempt
@login_required
def cmppost(request):
    print("🔹 Entered cmppost view")

    user_email = request.session.get('stremail')  # Get email from session
    print(f"🔹 Session Email: {user_email}")

    if not user_email:
        return HttpResponse("❌ No email found in session", status=400)

    login_instance = Login.objects.filter(stremail__iexact=user_email).first()
    if not login_instance:
        return HttpResponse("❌ User not found in Login table", status=404)

    # ✅ Restrict to Business/Organizations Only
    user_role = login_instance.user_type.lower().strip()
    if user_role != "organization" and user_role != "business":
        return HttpResponse("❌ Access denied. Only businesses can post here.", status=403)

    # Fetch associated organization
    organization_instance = Organization.objects.filter(login=login_instance).first()
    if not organization_instance:
        return HttpResponse("❌ Organization profile not found.", status=404)

    print(f"🔹 Organization Instance: {organization_instance}")

    user_posts = Post.objects.filter(login=login_instance).order_by('-postdttime')

    if request.method == 'POST':
        response = create_post_business(request)
        return response
    else:
        form = PostForm()

    return render(
        request,
        'cmppost.html',
        {
            'user_email': login_instance.stremail,
            'user_role': user_role,  # ✅ Ensure it matches the template
            'organization': organization_instance,
            'posts': user_posts,
            'form': form,
        }
    )'''

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
from .models import Post, Organization, Followers, Login

def cmppost(request, org_id):
    organization = Organization.objects.select_related("login").filter(id=org_id).first()

    if not organization:
        return HttpResponse("Organization not found", status=404)

    # 🔁 Annotate like counts per post
    posts = (
        Post.objects
        .filter(login__stremail=organization.stremail)
        .annotate(like_count=Count("likes"))
        .order_by('-id')
    )

    # 🧍 Current login user from session
    user_email = request.session.get("stremail")
    current_login = Login.objects.filter(stremail=user_email).first() if user_email else None

    # ✅ Track which posts are liked by current user
    liked_post_ids = []
    if current_login:
        liked_post_ids = Likes.objects.filter(login=current_login).values_list("post_id", flat=True)

    # ✅ Check follow status
    is_following = False
    if current_login and Followers.objects.filter(followid=org_id, login=current_login).exists():
        is_following = True

    follower_count = Followers.objects.filter(followid=org_id).count()

    return render(request, "cmppost.html", {
        "organization": organization,
        "posts": posts,
        "is_following": is_following,
        "follower_count": follower_count,
        "current_login": current_login,
        "liked_post_ids": list(liked_post_ids),  # ✅ Pass to template
    })


#for organization
from django.http import JsonResponse
from .models import Likes, Post, Login

def toggle_like(request, post_id):
    if request.method == "POST":
        user_email = request.session.get("stremail")
        if not user_email:
            return JsonResponse({"success": False, "error": "Not logged in"}, status=401)

        login = Login.objects.filter(stremail=user_email).first()
        if not login:
            return JsonResponse({"success": False, "error": "Invalid user"}, status=404)

        post = Post.objects.filter(id=post_id).first()
        if not post:
            return JsonResponse({"success": False, "error": "Post not found"}, status=404)

        # Check if already liked
        existing_like = Likes.objects.filter(login=login, post=post).first()
        if existing_like:
            existing_like.delete()
            status = "unliked"
        else:
            Likes.objects.create(login=login, post=post)
            status = "liked"

        like_count = Likes.objects.filter(post=post).count()
        return JsonResponse({"success": True, "status": status, "like_count": like_count})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=405)


from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Login, Post, Organization

def create_post_business(request, org_id):  # ✅ Accept org_id from URL
    if request.method == "POST":
        title = request.POST.get("posttitle")
        desc = request.POST.get("postdesc")
        image = request.FILES.get("postcontent")

        user_email = request.session.get("stremail")
        if not user_email:
            return HttpResponse("❌ No email found in session", status=400)

        login_instance = Login.objects.filter(stremail__iexact=user_email).first()
        if not login_instance:
            return HttpResponse("❌ User not found", status=404)

        user_role = login_instance.user_type.lower().strip()
        if user_role not in ["organization", "business"]:
            return HttpResponse("❌ Access denied. Only businesses can post here.", status=403)

        organization = Organization.objects.filter(id=org_id).first()  # ✅ Use org_id here
        if not organization:
            return HttpResponse("❌ Organization not found", status=404)

        new_post = Post(
            posttitle=title,
            postdesc=desc,
            postcontent=image,
            login=login_instance
        )
        new_post.save()

        return redirect("cmppost", org_id=organization.id)

    return HttpResponse("❌ Invalid request method", status=405)

    
from django.http import JsonResponse
from .models import Post, Login, Member, Organization, Agency

def get_posts(request):
    posts = Post.objects.all().order_by('-postdttime')
    post_list = []

    for post in posts:
        user = post.login
        username = ''
        profile_type = user.user_type
        profile_pic = ''

        # Get user name/email and profile photo
        if profile_type == 'jobseeker':
            member = Member.objects.filter(login=user).first()
            if member:
                username = member.eemail if member.eemail else user.stremail
                profile_pic = member.profile.url if member.profile else ''

        elif profile_type == 'business':
            org = Organization.objects.filter(login=user).first()
            if not org:
                org = Organization.objects.filter(stremail=user.stremail).first()
            if org:
                username = org.stremail if org.stremail else user.stremail
                profile_pic = org.logo.url if org.logo else ''

        elif profile_type == 'agency':
            agency = Agency.objects.filter(login=user).first()
            if agency:
                username = agency.email_address if agency.email_address else user.stremail
                profile_pic = agency.logo.url if agency.logo else ''

        post_list.append({
            'id': post.id,
            'posttitle': post.posttitle,
            'postdesc': post.postdesc,
            'postcontent': post.postcontent.url if post.postcontent else "",
            'username': username if username else user.stremail,
            'profile_pic': profile_pic if profile_pic else '/static/images/default-profile.png',
            'postdttime': post.postdttime.strftime("%Y-%m-%d %H:%M")
        })

    return JsonResponse(post_list, safe=False)




@csrf_exempt
@login_required
def delete_post(request, post_id):
    if request.method == "POST":
        user_email = request.session.get("stremail")
        login_instance = Login.objects.filter(stremail__iexact=user_email).first()

        post = Post.objects.filter(id=post_id, login=login_instance).first()
        if post:
            post.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Post not found or unauthorized"}, status=403)
    return JsonResponse({"error": "Invalid method"}, status=405)



from django.http import JsonResponse
from .models import Post, Login, Comments

def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("comment")
        user_email = request.session.get("stremail")

        if not user_email or not content:
            return JsonResponse({"success": False, "error": "Missing content or session."})

        login_instance = Login.objects.filter(stremail=user_email).first()
        if not login_instance:
            return JsonResponse({"success": False, "error": "User not found."})

        try:
            post = Post.objects.get(id=post_id)

            # Save the comment
            Comments.objects.create(
                post=post,
                login=login_instance,
                comments=content,
            )

            return JsonResponse({
                "success": True,
                "username": login_instance.stremail,
                "comment": content
            })
        except Post.DoesNotExist:
            return JsonResponse({"success": False, "error": "Post not found."})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

# views.py

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from .models import Comments, Login, Organization

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Validate user session
    user_email = request.session.get("stremail")
    login_instance = Login.objects.filter(stremail=user_email).first()

    # Authorization: only the comment owner or post owner can delete
    if comment.login != login_instance and comment.post.login != login_instance:
        return HttpResponse("❌ You don't have permission to delete this comment", status=403)

    # Get the organization for redirect
    org = Organization.objects.filter(login=comment.post.login).first()
    comment.delete()

    if org:
        return redirect("cmppost", org_id=org.id)
    return redirect("cmppost")  # fallback if org not found











from django.db.utils import IntegrityError
from .models import Organization, Member  # ensure this is imported

def business_info(request):
    """
    Handles organization registration with password encryption.
    """
    if request.method == "POST":
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                email = form.cleaned_data['stremail']

                # ✅ Check if this email already exists in Member table
                if Member.objects.filter(eemail=email).exists():
                    messages.error(request, "This email is already used by a jobseeker. Please use a different email.")
                    return redirect("business_info")

                organization = form.save(commit=False)

                # ✅ Encrypt the password before saving
                organization.set_password(form.cleaned_data['password'])

                # Save the organization to the database
                organization.save()
                messages.success(request, "Organization registered successfully!")
                print(f"Organization saved: {organization.cmpname}, Email: {organization.stremail}")
                return redirect(reverse("login"))

            except IntegrityError as e:
                messages.error(request, f"Registration failed due to integrity error: {str(e)}")
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
                print(f"Error saving organization: {str(e)}")
        else:
            messages.error(request, "Form validation failed. Please check your input.")
            print("Form errors:", form.errors)

    else:
        form = OrganizationForm()

    # Display all organizations for debugging and verification
    organizations = Organization.objects.all()
    print("All organizations:", organizations)

    return render(request, 'business_info.html', {
        'form': form,
        'organizations': organizations
    })


def agency_info(request):
    """
    Handles agency registration with password encryption.
    """
    if request.method == "POST":
        form = AgencyForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                agency = form.save(commit=False)

                # ✅ Encrypt the password before saving
                agency.set_password(form.cleaned_data['password'])

                agency.save()
                messages.success(request, "Agency registered successfully!")
                return redirect(reverse("login")) 
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
    else:
        form = AgencyForm()

    return render(request, 'agency_info.html', {'form': form})


def jobseeker(request):
    """
    Handles job seeker registration while preventing duplicate emails.
    """
    if request.method == "POST":
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('eemail')

            # Check if email already exists in Member
            if Member.objects.filter(eemail=email).exists():
                messages.error(request, "This email is already registered. Please log in.")
                return redirect('login')

            try:
                member = form.save(commit=False)

                # Encrypt password before saving
                encrypted_password = cipher.encrypt(form.cleaned_data['password'].encode()).decode()
                member.password = encrypted_password

                # ✅ Position is already handled by ModelChoiceField
                member.save()

                messages.success(request, "Member registered successfully! Please log in.")
                return redirect(reverse("login")) 

            except IntegrityError:
                messages.error(request, "This email is already registered. Please log in.")
            except Exception as e:
                messages.error(request, f"Registration failed: {str(e)}")
    else:
        form = MemberForm()

    return render(request, 'job_seeker.html', {'form': form})


def get_cities(request):
    state_id = request.GET.get('state_id')
    print("State ID Received:", state_id)  # Debugging
    if state_id:
        try:
            state_id = int(state_id)  # Convert to integer if necessary
            cities = City.objects.filter(state_id=state_id).values('id', 'cityname')
            print("Cities Found:", list(cities))  # Debugging
            return JsonResponse({"cities": list(cities)})
        except ValueError:
            print("Invalid State ID:", state_id)  # Debugging
            return JsonResponse({"cities": []})
    return JsonResponse({"cities": []})

def accounts(request):
    return render(request,'accounts.html')

def jobs(request):
    return render(request,'job_card.html')




from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from .models import Login, Post, Member, Organization, Agency, Likes, Comments

def homepage(request):
    query = request.GET.get('q', '').strip()
    all_members = []  # ✅ Initialize to avoid UnboundLocalError
    all_organizations = []  # ✅ Initialize to avoid UnboundLocalError
    all_agency = []

    if query:
        # 🔍 Search logic
        agency = Agency.objects.filter(agency_name__icontains=query).first()
        if agency:
            return redirect(reverse('public_agency_profile', args=[agency.id]))

        org = Organization.objects.filter(cmpname__icontains=query).first()
        if org:
            return redirect(reverse('user_profile', args=[org.id]))

        member = Member.objects.filter(
            Q(firstname__icontains=query) |
            Q(lastname__icontains=query) |
            Q(eemail__icontains=query)
        ).first()
        if member and member.login:
            return redirect(reverse('jobseeker_profile', args=[member.login.id]))

        all_members = Member.objects.select_related('login').all()
        all_organizations = Organization.objects.select_related('login').all()
        all_agency = Agency.objects.select_related('login').all()

        return render(request, 'homepage.html', {
            'query': query,
            'search_error': 'No matching user found.',
            'posts': [],
            'current_user_pic': '',
            'current_user_email': '',
            'all_members': all_members,
            'all_organizations': all_organizations,
            'all_agency': all_agency,
        })

    # 🧍 Sidebar info for current user
    current_user_pic = ''
    current_user_email = ''
    login_user = None
    current_org = None
    member = None
    agency = None
    user_email = request.session.get("stremail")

    if user_email:
        login_user = Login.objects.filter(stremail=user_email).first()
        if login_user:
            request.session["user_type"] = login_user.user_type

            if login_user.user_type == 'member':
                member = Member.objects.filter(login=login_user).first()
                if member:
                    current_user_email = member.eemail
                    current_user_pic = member.profile.url if member.profile else ''

            elif login_user.user_type == 'business':
                current_org = Organization.objects.filter(login=login_user).first() or Organization.objects.filter(stremail=user_email).first()
                if current_org:
                    current_user_email = current_org.stremail
                    current_user_pic = current_org.logo.url if current_org.logo else ''

            elif login_user.user_type == 'agency':
                agency = Agency.objects.filter(login=login_user).first()
                if agency:
                    current_user_email = agency.email_address
                    current_user_pic = agency.logo.url if agency.logo else ''

    # ✅ Get liked post IDs by current user
    liked_post_ids = Likes.objects.filter(login=login_user).values_list("post_id", flat=True) if login_user else []

    # 📰 Fetch all posts
    all_posts = Post.objects.select_related('login').order_by('-id')
    posts = []

    for post in all_posts:
        post_user = post.login
        post_email = ''
        post_profile_pic = ''
        post_profile_url = '#'

        try:
            if post_user.user_type == 'jobseeker':
                poster = Member.objects.filter(login=post_user).first()
                if poster:
                    post_email = poster.eemail
                    post_profile_url = reverse('member_profile', args=[poster.id])
                    post_profile_pic = poster.profile.url if poster.profile else ''

            elif post_user.user_type == 'business':
                org = Organization.objects.filter(login=post_user).first() or Organization.objects.filter(stremail=post_user.stremail).first()
                if org:
                    post_email = org.stremail
                    post_profile_url = reverse('user_profile', args=[post_user.id])
                    post_profile_pic = org.logo.url if org.logo else ''

            elif post_user.user_type == 'agency':
                post_agency = Agency.objects.filter(login=post_user).first()
                if post_agency:
                    post_email = post_agency.email_address
                    post_profile_url = reverse('public_agency_profile', args=[post_agency.id])
                    post_profile_pic = post_agency.logo.url if post_agency.logo else ''

        except Exception as e:
            print(f"[Post Error ID {post.id}] {e}")

        likes_count = Likes.objects.filter(post=post).count()
        comments_list = Comments.objects.filter(post=post).select_related('login').order_by('-commentsdate')

        posts.append({
            'id': post.id,
            'profile_pic': post_profile_pic,
            'postdesc': post.postdesc,
            'postcontent_url': post.postcontent.url if post.postcontent else '',
            'user_email': post_email,
            'profile_url': post_profile_url,
            'likes_count': likes_count,
            'comments': comments_list,
            'is_liked': post.id in liked_post_ids,
            'login_id': post.login.id if post.login else None,
        })

    # ✅ Get all members for suggestion (excluding self if needed)
    all_members = Member.objects.exclude(login=login_user) if login_user else Member.objects.all()
    all_organizations = Organization.objects.exclude(login=login_user) if login_user else Organization.objects.all()
    all_agency = Agency.objects.exclude(login=login_user) if login_user else Agency.objects.all()

    return render(request, 'homepage.html', {
        'posts': posts,
        'current_user_pic': current_user_pic,
        'current_user_email': current_user_email,
        'organization': current_org,
        'member': member,
        'agency': agency,
        'all_members': all_members,
        'all_organizations': all_organizations,
        'all_agency': all_agency,
    })



from django.http import JsonResponse
from .models import Post, Likes, Login

def toggle_like_member(request, post_id):
    if request.method == "POST":
        user_email = request.session.get("stremail")
        if not user_email:
            return JsonResponse({"success": False, "error": "User not logged in"}, status=403)

        login_user = Login.objects.filter(stremail=user_email).first()
        if not login_user:
            return JsonResponse({"success": False, "error": "Login not found"}, status=404)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"success": False, "error": "Post not found"}, status=404)

        like, created = Likes.objects.get_or_create(post=post, login=login_user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Likes.objects.filter(post=post).count()
        return JsonResponse({"success": True, "liked": liked, "like_count": like_count})

    return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Post, Comments, Login

@csrf_exempt
def add_comment_member(request, post_id):
    if request.method == "POST":
        content = request.POST.get("comment")
        user_email = request.session.get("stremail")

        if not content or not user_email:
            return JsonResponse({"success": False, "error": "Missing content or login"})

        login_user = Login.objects.filter(stremail=user_email).first()
        post = Post.objects.filter(id=post_id).first()

        if not login_user or not post:
            return JsonResponse({"success": False, "error": "User or post not found"})

        Comments.objects.create(post=post, login=login_user, comments=content)
        return JsonResponse({"success": True, "comment": content, "username": user_email})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=405)

#hiring
from django.shortcuts import render, get_object_or_404
from .models import Job, Application
from django.urls import reverse

def hiring_view(request, job_id):
    job = get_object_or_404(Job.objects.select_related("city", "city__state"), id=job_id)

    # ✅ Handle application status update
    if request.method == 'POST':
        app_id = request.POST.get("applicationid")
        new_status = request.POST.get("status")
        if app_id and new_status:
            app = Application.objects.filter(id=app_id, job=job).first()
            if app:
                app.status = new_status
                app.save()

    # ✅ Get all applications for this job
    applications = Application.objects.filter(job=job).select_related("member", "member__login")

    org_job_list_url = None
    if job.organization:
        org_job_list_url = reverse('list_job', args=[job.organization.id])

    # ✅ Categorize based on status
    pending_applications = applications.filter(status="Pending")
    shortlist_applications = applications.filter(status="ShortList")
    rejected_applications = applications.filter(status="Reject")

    return render(request, 'hiring.html', {
        'job': job,
        'applications': pending_applications,            # For "All Applied"
        'shortlistapplications': shortlist_applications,
        'rejectedapplications': rejected_applications,
        'org_job_list_url': org_job_list_url,  # 👈 added
    })


#list of jobs
from django.shortcuts import render, get_object_or_404
from .models import Job, Organization

def list_job(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    jobs = Job.objects.filter(organization=organization, agency__isnull=True)  # exclude agency reposts if needed

    return render(request, 'joblist.html', {
        'organization': organization,
        'jobs': jobs
    })



def member_profile(request, id):
    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        messages.error(request, "Member not found.")
        return redirect('homepage')

    # Fetch related data
    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    posts = Post.objects.filter(login=member.login).order_by("-postdttime")

    try:
        summary = Summary.objects.get(member=member)
    except Summary.DoesNotExist:
        summary = None

    return render(request, 'new_profile.html', {
        'member': member,
        'summary': summary,
        'education': education,
        'skills': skills,
        'experience': experience,
        'languages': languages,
        'links': links,
        'posts': posts,
    })









from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from .models import Login, Member, Agency, Organization, Post, Job, Followers

def user_profile(request, login_id):
    login_user = get_object_or_404(Login, id=login_id)
    session_email = request.session.get("stremail")

    # ✅ Check if user is an Organization
    try:
        org = Organization.objects.get(login=login_user)
        posts = Post.objects.filter(login=login_user).order_by("-id")
        jobs = Job.objects.filter(organization=org, agency__isnull=True).order_by("-id")[:3]
        follower_count = Followers.objects.filter(followid=org.id).count()
        is_following = Followers.objects.filter(followid=org.id, login__stremail=session_email).exists()
        return render(request, "cmphome1.html", {
            "profile": org,
            "user_type": "business",
            "tab": request.GET.get("tab", "home"),
            "posts": posts,
            "jobs": jobs,
            "follower_count": follower_count,
            "is_following": is_following,
        })
    except Organization.DoesNotExist:
        pass

    # ✅ Check if user is an Agency
    try:
        agency = Agency.objects.get(login=login_user)
        jobs = Job.objects.filter(agency=agency).order_by("-id")[:3]
        follower_count = Followers.objects.filter(followid=agency.id).count()
        is_following = Followers.objects.filter(followid=agency.id, login__stremail=session_email).exists()
        return render(request, "agency_profile.html", {
            "agency": agency,
            "user_type": "agency",
            "jobs": jobs,
            "follower_count": follower_count,
            "is_following": is_following,
        })
    except Agency.DoesNotExist:
        pass

    # ✅ Check if user is a Member (Job Seeker)
    try:
        member = Member.objects.get(login=login_user)
        posts = Post.objects.filter(login=login_user).order_by("-id")
        follower_count = Followers.objects.filter(followid=member.id).count()
        is_following = Followers.objects.filter(followid=member.id, login__stremail=session_email).exists()
        return render(request, "new_profile1.html", {
            "member": member,
            "user_type": "jobseeker",
            "posts": posts,
            "follower_count": follower_count,
            "is_following": is_following,
        })
    except Member.DoesNotExist:
        pass

    return HttpResponseNotFound("\u274c No valid profile found for this user.")

from django.shortcuts import render, get_object_or_404
from .models import Login, Organization

def user_about(request, login_id):
    login_user = get_object_or_404(Login, id=login_id)
    profile = get_object_or_404(Organization, login=login_user)

    # Optional: check profile.id is valid
    print("ORG ID:", profile.id)

    # Safely parse values if needed
    import ast
    try:
        values_list = ast.literal_eval(profile.values) if profile.values else []
    except:
        values_list = []

    # Example: follower count & following check
    follower_count = Followers.objects.filter(followid=profile.id).count()
    is_following = Followers.objects.filter(followid=profile.id, login__stremail=request.session.get("stremail")).exists()

    return render(request, "cmpabout1.html", {
        'profile': profile,
        'values_list': values_list,
        'follower_count': follower_count,
        'is_following': is_following,
    })


from django.db.models import Count, Prefetch
from .models import Post, Login, Followers, Likes, Comments, Organization

def user_posts(request, login_id):
    login_user = get_object_or_404(Login, id=login_id)
    profile = get_object_or_404(Organization, login=login_user)

    # Annotate like count
    post_queryset = (
        Post.objects.filter(login=login_user)
        .annotate(like_count=Count("likes"))
        .order_by('-id')
    )

    # Current logged-in user
    current_login = Login.objects.filter(stremail=request.session.get("stremail")).first()
    liked_post_ids = Likes.objects.filter(login=current_login).values_list("post_id", flat=True) if current_login else []

    # Fetch followers
    follower_count = Followers.objects.filter(followid=profile.id).count()
    is_following = Followers.objects.filter(followid=profile.id, login=current_login).exists()

    # ✅ Combine posts with their comments
    post_list = []
    for post in post_queryset:
        comments = Comments.objects.filter(post=post).select_related("login").order_by("-commentsdate")
        
        post_list.append({
            "id": post.id,
            "posttitle": post.posttitle,
            "postdesc": post.postdesc,
            "postdttime": post.postdttime,
            "postcontent": post.postcontent,
            "like_count": post.like_count,
            "comments": comments,
            "is_liked": post.id in liked_post_ids,
            "login_id": post.login.id if post.login else None,   # ✅ Add this
            "user_email": post.login.stremail if post.login else "",  # ✅ Optional
            "login": post.login,  # ✅ THIS IS THE FIX
        })

    return render(request, "cmppost1.html", {
        "profile": profile,
        "posts": post_list,
        "follower_count": follower_count,
        "is_following": is_following,
        "liked_post_ids": list(liked_post_ids),
    })


from django.shortcuts import render, get_object_or_404
from .models import Job, Login, Organization, Followers

def user_jobs(request, login_id):
    # 1. Get the organization profile by login_id
    login_user = get_object_or_404(Login, id=login_id)
    profile = get_object_or_404(Organization, login=login_user)

    # 2. Get all jobs posted by this organization
    jobs = Job.objects.filter(organization=profile).select_related("organization")

    # 3. Get follower count for this organization
    follower_count = Followers.objects.filter(followid=profile.id).count()
    job_count = jobs.count()

    # 4. Check if the currently logged-in user is following
    is_following = False
    user_email = request.session.get("stremail")
    if user_email:
        login = Login.objects.filter(stremail=user_email).first()
        if login:
            is_following = Followers.objects.filter(
                followid=profile.id,
                login=login
            ).exists()

    # 5. Render the organization's job page without affecting the session
    return render(request, "cmpjob1.html", {
        'profile': profile,  # organization profile being visited
        'follower_count': follower_count,
        'is_following': is_following,
        'jobs': jobs,
        'job_count': job_count,
    })


def jobseeker_profile(request, login_id):
    login_user = get_object_or_404(Login, id=login_id)
    
    if login_user.user_type == 'jobseeker':
        member = get_object_or_404(Member, login=login_user)
        
        # Fetch related objects
        summary = Summary.objects.filter(member=member).first()
        posts = Post.objects.filter(login=login_user).order_by('-id')  # Assuming login foreign key in Post
        experience = MemberExperience.objects.filter(member=member).order_by('-startdate')
        education = MemberEducation.objects.filter(member=member).order_by('-passingyear')
        skills = MemberSkills.objects.filter(member=member)
        links = MemberLink.objects.filter(member=member)
        languages = MemberLanguage.objects.filter(member=member)

        return render(request, 'new_profile1.html', {
            'member': member,
            'summary': summary,
            'posts': posts,
            'experience': experience,
            'education': education,
            'skills': skills,
            'links': links,
            'languages': languages,
        })

    return HttpResponseNotFound("User type not supported")


#agency homepage from agency
from django.shortcuts import render, get_object_or_404, redirect
from .models import Agency, Organization, Job, Followers
from django.contrib import messages

def agency_homepage(request):
    login_id = request.session.get("login_id")
    print("🔐 login_id from session:", login_id)

    try:
        agency = Agency.objects.get(login__id=login_id)
        print("✅ Agency found:", agency)
    except Agency.DoesNotExist:
        print("❌ No agency found with login_id =", login_id)
        messages.error(request, "Agency not found.")
        return redirect("login")

    # Get recent 3 jobs posted by the agency (not organization)
    recent_jobs = Job.objects.filter(agency=agency).order_by('-applystartdate')[:3]

    follower_count = Followers.objects.filter(followid=agency.id).count()
    is_following = Followers.objects.filter(
        followid=agency.id,
        login__stremail=request.session.get("stremail")
    ).exists()

    return render(request, "agency_homepage.html", {
        "agency": agency,
        "recent_jobs": recent_jobs,
        "follower_count": follower_count,
        "is_following": is_following
    })

from .models import Job, Agency, Organization

def agency_jobs(request):
    login_id = request.session.get("login_id")
    agency = get_object_or_404(Agency, login_id=login_id)

    agency_jobs = Job.objects.filter(agency=agency)  # Jobs posted by this agency
    organization_jobs = Job.objects.filter(organization__isnull=False, agency__isnull=True).order_by('-id')  # Jobs posted by organizations

    return render(request, "agency_job.html", {
        "agency": agency,
        "jobs": agency_jobs,              # Agency jobs shown normally
        "organization_jobs": organization_jobs,  # Available org jobs to pick and post
        "job_count": agency_jobs.count(),
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_agency_info(request):
    if request.method == "POST":
        agency_id = request.session.get("login_id")
        intro = request.POST.get("companyIntroduction")
        overview = request.POST.get("companyOverview")

        try:
            agency = Agency.objects.get(login_id=agency_id)
            agency.intro = intro
            agency.overview = overview
            agency.save()
            return JsonResponse({"success": True})
        except Agency.DoesNotExist:
            return JsonResponse({"success": False, "message": "Agency not found"})
    return JsonResponse({"success": False, "message": "Invalid request"})

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from myapp.models import Job, Agency, Organization

@csrf_exempt
def duplicate_jobs_to_agency(request):
    if request.method == "POST":
        data = json.loads(request.body)
        job_ids = data.get("job_ids", [])

        login_id = request.session.get("login_id")
        try:
            agency = Agency.objects.get(login_id=login_id)
        except Agency.DoesNotExist:
            return JsonResponse({"success": False, "error": "Agency not found."})

        for job_id in job_ids:
            try:
                job = Job.objects.get(id=job_id)

                # Create a new job for the agency
                Job.objects.create(
                    organization=job.organization,
                    agency=agency,
                    cmpname=job.cmpname,
                    position=job.position,
                    noofvacancies=job.noofvacancies,
                    requiredqualification=job.requiredqualification,
                    requiredexperience=job.requiredexperience,
                    jobdescription=job.jobdescription,
                    jobtype=job.jobtype,
                    city=job.city,
                    applystartdate=job.applystartdate,
                    lastdate=job.lastdate,
                    skillsrequired=job.skillsrequired,
                    salary=job.salary,
                    post=job.post
                )
            except Job.DoesNotExist:
                continue  # Skip invalid job IDs

        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})

#agency from other user
def public_agency_profile(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)
    follower_count = Followers.objects.filter(followid=agency.id).count()
    is_following = Followers.objects.filter(
        followid=agency.id,
        login__stremail=request.session.get("stremail")
    ).exists()
    recent_jobs = Job.objects.filter(agency=agency).order_by('-applystartdate')[:3]

    return render(request, "agency_homepage1.html", {
        "agency": agency,
        "recent_jobs": recent_jobs,
        "follower_count": follower_count,
        "is_following": is_following,
    })

from .models import Login, Organization, Job

def public_agency_jobs(request, agency_id):
    agency = get_object_or_404(Agency, id=agency_id)

    # 👇 Identify the current logged-in user from session
    user_email = request.session.get('stremail')
    current_org = None
    org_jobs = None

    if user_email:
        login = Login.objects.filter(stremail=user_email).first()
        current_org = Organization.objects.filter(login=login).first()

        if current_org:
            org_jobs = Job.objects.filter(organization=current_org).order_by('-applystartdate')

    # Agency posted jobs
    agency_jobs = Job.objects.filter(agency=agency).order_by('-applystartdate')

    follower_count = Followers.objects.filter(followid=agency.id).count()
    is_following = Followers.objects.filter(followid=agency.id, login__stremail=user_email).exists()

    return render(request, "agency_jobs1.html", {
        "agency": agency,
        "agency_jobs": agency_jobs,
        "org_jobs": org_jobs,  # 👈 Now you have access to current org's jobs
        "follower_count": follower_count,
        "is_following": is_following,
    })




from datetime import date
from dateutil.relativedelta import relativedelta

def add_cv(request):
    # ✅ Ensure user is logged in
    if not request.session.get('is_logged_in'):
        messages.error(request, "You are not logged in.")
        return redirect(reverse('login'))

    user_email = request.session.get('stremail')  # ✅ Fix this
    user_type = request.session.get('user_type')

    try:
        if user_type == "jobseeker" or user_type == "member":
            member = Member.objects.get(eemail=user_email)
        elif user_type == "agency":
            member = Agency.objects.get(email_address=user_email)
        elif user_type == "business":
            member = Organization.objects.get(stremail=user_email)
        else:
            messages.error(request, "Invalid user type.")
            return redirect(reverse('login'))

    except (Member.DoesNotExist, Agency.DoesNotExist, Organization.DoesNotExist):
        messages.error(request, "Profile not found.")
        return redirect(reverse('login'))

    # ✅ Form Handling
    if request.method == "POST":
        if "summary_form" in request.POST:
            summary_text = request.POST.get("summary")
            if summary_text:
                Summary.objects.create(member=member, summary=summary_text)
                messages.success(request, "Summary added successfully!")
                return redirect(reverse('add_cv'))  # ✅ Fix Redirect
            else:
                messages.error(request, "Error adding summary.")

        elif "education_form" in request.POST:
            edu_form = MemberEducationForm(request.POST)
            if edu_form.is_valid():
                education = edu_form.save(commit=False)
                education.member = member
                education.save()
                messages.success(request, "Education added successfully!")
                return redirect(reverse('add_cv'))  # ✅ Fix Redirect
            
        elif "skills_form" in request.POST:
            skills_form = MemberSkillsForm(request.POST)
            if skills_form.is_valid():
                skills = skills_form.save(commit=False)
                skills.member = member
                skills.save()
                messages.success(request, "Skills added successfully!")
                return redirect('/cv')
            else:
                messages.error(request, "Error adding skills. Please check the form.")

        elif "experience_form" in request.POST:
            exp_form = MemberExperienceForm(request.POST)
            if exp_form.is_valid():
                experience = exp_form.save(commit=False)
                experience.member = member

                # 🔢 Auto-calculate total months of experience
                end = experience.enddate if experience.enddate else date.today()
                delta = relativedelta(end, experience.startdate)
                experience.totalmonthexperience = delta.years * 12 + delta.months

                experience.save()
                messages.success(request, "Experience added successfully!")
                return redirect('/cv')



        elif "language_form" in request.POST:
            lang_form = MemberLanguageForm(request.POST)
            if lang_form.is_valid():
                language = lang_form.save(commit=False)
                language.member = member
                language.save()
                messages.success(request, "Language added successfully!")
                return redirect('/cv')
            else:
                messages.error(request, "Error adding language. Please check the form.")

        elif "link_form" in request.POST:
            link_form = MemberLinkForm(request.POST)
            if link_form.is_valid():
                link = link_form.save(commit=False)
                link.member = member
                link.save()
                messages.success(request, "Link added successfully!")
                return redirect('/cv')
            else:
                messages.error(request, "Error adding link. Please check the form.")

        # ✅ Fetch existing CV details
    education = MemberEducation.objects.filter(member=member)
    skills = MemberSkills.objects.filter(member=member)
    experience = MemberExperience.objects.filter(member=member)
    languages = MemberLanguage.objects.filter(member=member)
    links = MemberLink.objects.filter(member=member)
    summary = Summary.objects.filter(member=member)

    # ✅ Calculate total experience in months
    total_months = 0
    for exp in experience:
        end = exp.enddate if exp.enddate else date.today()
        delta = relativedelta(end, exp.startdate)
        months = delta.years * 12 + delta.months
        total_months += months

    # Create empty forms for displaying on page load
    edu_form = MemberEducationForm()
    skills_form = MemberSkillsForm()
    exp_form = MemberExperienceForm()
    lang_form = MemberLanguageForm()
    link_form = MemberLinkForm()

    context = {
        'member': member,
        'education': education,
        'skills': skills,
        'experience': experience,
        'languages': languages,
        'links': links,
        'summary': summary,
        'edu_form': edu_form,
        'skills_form': skills_form,
        'exp_form': exp_form,
        'lang_form': lang_form,
        'link_form': link_form,
        'total_experience_months': total_months,
    }

    return render(request, 'cv_builder.html', context)



from django.shortcuts import get_object_or_404

def delete_education(request, edu_id):
    education = get_object_or_404(MemberEducation, id=edu_id)
    education.delete()
    messages.success(request, "Education deleted successfully!")
    return redirect('/cv')

from django.shortcuts import get_object_or_404

def delete_summary(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id)
    summary.delete()
    messages.success(request, "Summary deleted successfully!")
    return redirect('/cv')

from django.shortcuts import get_object_or_404

def delete_skill(request, skill_id):
    skill = get_object_or_404(MemberSkills, id=skill_id)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect('/cv')

from django.shortcuts import get_object_or_404

def delete_experience(request, exp_id):
    experience = get_object_or_404(MemberExperience, id=exp_id)
    experience.delete()
    messages.success(request, "Experience deleted successfully!")
    return redirect('/cv')

from django.shortcuts import get_object_or_404

def delete_language(request, lang_id):
    language = get_object_or_404(MemberLanguage, id=lang_id)
    language.delete()
    messages.success(request, "Language deleted successfully!")
    return redirect('/cv')

from django.shortcuts import get_object_or_404

def delete_link(request, link_id):
    link = get_object_or_404(MemberLink, id=link_id)
    link.delete()
    messages.success(request, "Link deleted successfully!")
    return redirect('/cv')

def cv_success(request):
    return render(request,'cv_seccess.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    Member, Agency, Organization, Login, Post,
    MemberEducation, MemberSkills, MemberExperience,
    MemberLanguage, MemberLink, Summary
)

def new_profile_view(request):
    """Profile Page View for the Logged-in User"""

    # ✅ Retrieve session values
    email = request.session.get("stremail")
    user_type = request.session.get("user_type")

    if not email or not user_type:
        return redirect("login")

    # ✅ Get Login object
    try:
        login_user = Login.objects.get(stremail=email)
    except Login.DoesNotExist:
        messages.error(request, "Login not found.")
        return redirect("login")

    user_data = None
    education = skills = experience = languages = links = summary = None

    # ✅ Fetch data based on user_type
    if user_type == "jobseeker":
        try:
            user_data = Member.objects.get(eemail=email)

            # Education, skills, experience, etc.
            education = MemberEducation.objects.filter(member=user_data)
            skills = MemberSkills.objects.filter(member=user_data)
            experience = MemberExperience.objects.filter(member=user_data)
            languages = MemberLanguage.objects.filter(member=user_data)
            links = MemberLink.objects.filter(member=user_data)

            # Summary (safe check)
            try:
                summary = Summary.objects.get(member=user_data)
            except Summary.DoesNotExist:
                summary = None

        except Member.DoesNotExist:
            messages.error(request, "Member profile not found.")
            return redirect("logout")

    elif user_type == "agency":
        try:
            user_data = Agency.objects.get(email_address=email)
        except Agency.DoesNotExist:
            messages.error(request, "Agency profile not found.")
            return redirect("logout")

    elif user_type == "business":
        try:
            user_data = Organization.objects.get(stremail=email)
        except Organization.DoesNotExist:
            messages.error(request, "Organization profile not found.")
            return redirect("logout")

    # ✅ Fetch posts for the login user
    posts = Post.objects.filter(login=login_user).order_by("-postdttime")
    post_count = posts.count()  # ✅ Total number of posts

    follower_count = 0
    if user_type == "jobseeker":
        follower_count = Followers.objects.filter(followid=user_data.id).count()


    # ✅ Handle new post creation
    if request.method == "POST" and user_type == "jobseeker":
        posttitle = request.POST.get("posttitle")
        postdesc = request.POST.get("postdesc")
        postcontent = request.FILES.get("postcontent")

        if posttitle and postdesc:
            new_post = Post(
                login=login_user,
                posttitle=posttitle,
                postdesc=postdesc,
                postcontent=postcontent if postcontent else None
            )
            try:
                new_post.save()
                return redirect("new_profile_view")
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=500)
        else:
            return JsonResponse({"success": False, "error": "Missing title or description."})

    # ✅ Final context
    context = {
        "user_type": user_type,
        "user_data": user_data,
        "member": user_data if user_type == "jobseeker" else None,
        "education": education,
        "skills": skills,
        "experience": experience,
        "languages": languages,
        "links": links,
        "summary": summary,
        "posts": posts,
        "post_count": post_count,
        "follower_count": follower_count,
    }

    return render(request, "new_profile.html", context)




#@login_required
'''def create_post(request):
    if request.method == "POST":
        print("Received POST request:", request.POST)
        print("Received FILES:", request.FILES)

        post_title = request.POST.get("posttitle")
        post_desc = request.POST.get("postdesc")
        post_content = request.FILES.get("postcontent")

        if not post_title or not post_desc:
            return JsonResponse({"success": False, "error": "Title and caption are required"}, status=400)

        # ✅ Ensure the correct user association with Login table
        try:
            user_login = Login.objects.get(user=request.user)  # Ensure user exists in Login table
        except Login.DoesNotExist:
            return JsonResponse({"success": False, "error": "User not found in Login table"}, status=400)

        # ✅ Create and save the post
        post = Post(
            login=user_login,  
            posttitle=post_title,
            postdesc=post_desc,
        )

        # ✅ Save post content if uploaded
        if post_content:
            post.postcontent = post_content

        post.save()

        # ✅ Check if "See All Posts" should be shown
        total_posts = Post.objects.filter(login=user_login).count()
        show_see_all_link = total_posts > 3  # Only show if more than 3 posts

        return JsonResponse({
            "success": True,
            "message": "Post created successfully!",
            "show_see_all_link": show_see_all_link
        })

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)'''
'''from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Login
import traceback

@csrf_exempt  # Allows AJAX requests without CSRF token
def create_post(request):
    if request.method == "POST":
        try:
            print("\n🔹 DEBUG: Session Data:", request.session.items())  # Debugging session storage

            post_title = request.POST.get("posttitle")
            post_desc = request.POST.get("postdesc")
            post_content = request.FILES.get("postcontent")

            if not post_title or not post_desc:
                print("❌ ERROR: Missing title or description")
                return JsonResponse({"success": False, "error": "Title and caption are required"}, status=400)

            # ✅ Fetch user email from session
            user_email = request.session.get("stremail")  # 🔹 Fix: Use 'stremail' from session
            if not user_email:
                return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

            # ✅ Ensure the user exists in the Login table
            try:
                user_login = Login.objects.get(stremail=user_email)
            except Login.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found in Login table"}, status=400)

            # ✅ Create and save the post
            post = Post(
                login=user_login,  
                posttitle=post_title,
                postdesc=post_desc,
            )

            if post_content:
                post.postcontent = post_content

            post.save()

            print("✅ SUCCESS: Post created!")

            # ✅ Check if "See All Posts" should be shown
            total_posts = Post.objects.filter(login=user_login).count()
            show_see_all_link = total_posts > 3  

            return JsonResponse({
                "success": True,
                "message": "Post created successfully!",
                "show_see_all_link": show_see_all_link
            })

        except Exception as e:
            print("🔥 SERVER ERROR:", str(e))
            print(traceback.format_exc())  # Prints detailed error traceback
            return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse  # Import for URL redirection
from .models import Post, Login
import traceback

@csrf_exempt  
def create_post_jobseeker(request):
    if request.method == "POST":
        try:
            print("\n🔹 DEBUG: Session Data:", request.session.items())  

            post_title = request.POST.get("posttitle")
            post_desc = request.POST.get("postdesc")
            post_content = request.FILES.get("postcontent")

            if not post_title or not post_desc:
                print("❌ ERROR: Missing title or description")
                return JsonResponse({"success": False, "error": "Title and caption are required"}, status=400)

            # ✅ Fetch user email from session
            user_email = request.session.get("stremail")  
            if not user_email:
                return JsonResponse({"success": False, "error": "User not authenticated"}, status=401)

            # ✅ Ensure the user exists in the Login table
            try:
                user_login = Login.objects.get(stremail=user_email)
            except Login.DoesNotExist:
                return JsonResponse({"success": False, "error": "User not found in Login table"}, status=400)

            # ✅ Create and save the post
            post = Post(
                login=user_login,  
                posttitle=post_title,
                postdesc=post_desc,
            )

            if post_content:
                post.postcontent = post_content

            post.save()

            print("✅ SUCCESS: Post created!")

            # ✅ Count total posts by the user
            total_posts = Post.objects.filter(login=user_login).count()

            # ✅ Determine if "See All Posts" should be shown
            show_see_all_link = total_posts > 3  

            # ✅ Add redirect URL if the fourth post is added
            redirect_url = reverse("see_all_posts") if total_posts == 4 else None

            return JsonResponse({
                "success": True,
                "message": "Post created successfully!",
                "show_see_all_link": show_see_all_link,
                "redirect_url": redirect_url  # 🔹 Redirect user when the fourth post is added
            })

        except Exception as e:
            print("🔥 SERVER ERROR:", str(e))
            print(traceback.format_exc())  
            return JsonResponse({"success": False, "error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)






from django.shortcuts import render
from .models import Post, Login

def see_all_posts(request):
    try:
        # ✅ Get logged-in user's email from session
        user_email = request.session.get("stremail")
        
        if not user_email:
            return render(request, "see_all_posts.html", {"error": "User not authenticated"})

        # ✅ Fetch the user's login entry
        user_login = Login.objects.get(stremail=user_email)  

        # ✅ Fetch all posts for this user (including images)
        posts = Post.objects.filter(login=user_login).order_by("-id")  

        return render(request, "see_all_posts.html", {"posts": posts})

    except Login.DoesNotExist:
        return render(request, "see_all_posts.html", {"error": "User not found in Login table"})





def logout_view(request):
    if request.user.is_authenticated:
        # Remove session from the corresponding model
        model_instance = None
        login_instance = None
        
        try:
            login_instance = Login.objects.get(stremail=request.user.email)  # Adjust this if necessary
        except Login.DoesNotExist:
            pass

        if login_instance:
            for model in [Member, Agency, Organization]:
                try:
                    model_instance = model.objects.get(login=login_instance)  # Using 'login' instead of 'user'
                    break
                except model.DoesNotExist:
                    pass

            # Clear session key if found
            if model_instance:
                model_instance.session_key = None
                model_instance.save()

        # Logout user
        logout(request)
        messages.success(request, "You have been logged out successfully!")

    return redirect('firstpage')
