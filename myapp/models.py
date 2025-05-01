from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
from django.utils.timezone import now   #for login

from django.conf import settings
from cryptography.fernet import Fernet

# Ensure settings.ENCRYPTION_KEY is accessed properly
cipher = Fernet(settings.ENCRYPTION_KEY.encode())  # Fix this line

class Login(models.Model):
    id = models.AutoField(primary_key=True)
    stremail = models.EmailField(unique=True)
    password = models.CharField(max_length=500)  # Encrypted password
    user_type = models.CharField(max_length=20, null=True, blank=True)
    last_login = models.DateTimeField(default=now)

    class Meta:
        db_table = "login"

    def set_password(self, raw_password):
        """Encrypt and store the password."""
        if not raw_password.startswith("gAAAA"):  # Avoid double encryption
            self.password = cipher.encrypt(raw_password.encode()).decode()

    def check_password(self, raw_password):
        """Decrypt and verify the password."""
        try:
            if self.password.startswith("gAAAA"):  # Only decrypt if it's encrypted
                decrypted_password = cipher.decrypt(self.password.encode()).decode()
                return decrypted_password == raw_password
            return self.password == raw_password  # Compare directly if not encrypted
        except Exception:
            return False  

    def __str__(self):
        return f"{self.stremail} ({self.user_type})"


class State(models.Model):
    id = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=100)

    class Meta: 
        db_table = "state"
    
    def __str__(self):  
        return self.sname

class City(models.Model):
    id = models.AutoField(primary_key=True)
    cityname = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table = "city"
        unique_together = ('state', 'cityname')  

    def __str__(self):  
        return self.cityname

cipher = Fernet(settings.ENCRYPTION_KEY.encode())

class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    agency_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email_address = models.EmailField()
    website = models.URLField(max_length=200, null=True, blank=True)
    logo = models.ImageField(upload_to='agency_logos/', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='agency_city')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='agency_state')
    date_of_establishment = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    intro = models.TextField(max_length=300,blank=True,null=True)
    overview = models.TextField(max_length=500,blank=True,null=True)

    class Meta:
        db_table = "agency"

    def __str__(self):
        return f"{self.agency_name} ({self.email_address})"

    
    def set_password(self, raw_password):
        """Encrypts the password before saving it."""
        self.password = cipher.encrypt(raw_password.encode()).decode()
        self.save()

    def decrypt_password(self):
        """Decrypts the stored password."""
        try:
            return cipher.decrypt(self.password.encode()).decode()
        except Exception:
            return "Error decrypting password"

class CompanyCategory(models.Model):
    id = models.AutoField(primary_key=True)
    ccname = models.CharField(max_length=100)

    class Meta:
        db_table = "company_category"
    
    def __str__(self):
        return self.ccname
    

class Positions(models.Model):
    id = models.AutoField(primary_key=True)
    positionname = models.CharField(max_length=100)
    companycategory = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = "positions"

    def __str__(self):
        return self.positionname


from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

# Initialize cipher
cipher = Fernet(settings.ENCRYPTION_KEY.encode())

class Organization(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, blank=True)
    cmpname = models.CharField(max_length=100)
    password = models.CharField(max_length=500)  # Stores encrypted password
    stremail = models.EmailField(unique=True)
    logo = models.ImageField(upload_to='logos/',null=True,blank=True)
    strmobileno = models.CharField(max_length=20)
    website = models.URLField(max_length=200, null=True, blank=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    intro = models.TextField(max_length=300,blank=True,null=True)
    overview = models.TextField(max_length=500,blank=True,null=True)
    mission = models.TextField(max_length=500,blank=True,null=True)
    vision = models.TextField(max_length=500,blank=True,null=True)
    values = models.JSONField(default=list, blank=True, null=True)

    STATUS_CHOICES = [('active', 'Active'), ('inactive', 'Inactive'), ('pending', 'Pending')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    ccid = models.ForeignKey('CompanyCategory', on_delete=models.CASCADE, null=True, blank=True, default=1)
    cmp_strength = models.IntegerField(blank=True, null=True)

    def set_password(self, raw_password):
        """Encrypts the password before saving it."""
        self.password = cipher.encrypt(raw_password.encode()).decode()
        self.save()

    def decrypt_password(self):
        """Decrypts the stored password."""
        try:
            return cipher.decrypt(self.password.encode()).decode()
        except Exception:
            return "Error decrypting password"

    def __str__(self):
        return f"{self.cmpname} ({self.stremail})"

    class Meta:
        db_table = "organization"


from cryptography.fernet import Fernet
from django.conf import settings

ENCRYPTION_KEY = settings.ENCRYPTION_KEY.encode()
cipher = Fernet(ENCRYPTION_KEY)

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    #login = models.ForeignKey(Login, on_delete=models.CASCADE,null=True)
    login = models.OneToOneField(Login, on_delete=models.CASCADE, null=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    profile = models.ImageField(upload_to='profile/', null=True, blank=True)
    eemail = models.EmailField(blank=True,null=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    position = models.ForeignKey(Positions, on_delete = models.CASCADE,null=True)

    def decrypt_password(self):
        try:
            return cipher.decrypt(self.password.encode()).decode() if self.password else None
        except Exception:
            return None  # Avoid exposing errors

    def save(self, *args, **kwargs):
        """Encrypt password before saving to the database."""
        if self.password and not self.password.startswith("gAAAAA"):  # Avoid re-encrypting
            self.password = cipher.encrypt(self.password.encode()).decode()
        super().save(*args, **kwargs)

        
    class Meta:
        db_table = "member"

    def __str__(self):
        return self.eemail if self.eemail else f"Member {self.id}"


class Summary(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    summary = models.TextField(blank=True,null=True)

    class Meta:
        db_table = "summary"

    def __str__(self):
        return f"{self.member.eemail} - summary"
    

class MemberEducation(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    passingyear = models.CharField(max_length=255)
    institute = models.CharField(max_length=100)
    grade = models.CharField(max_length=20)
    remark = models.CharField(max_length=20)

    class Meta:
        db_table = "membereducation"

class MemberSkills(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    skills = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

    class Meta:
        db_table = "memberskills"
    
    def __str__(self):
        return self.skills

class MemberExperience(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    organizationname = models.CharField(max_length=100)  # Instead of 'company'
    worktitle = models.CharField(max_length=100)  # Instead of 'position'
    workdetails = models.TextField()
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    totalmonthexperience = models.IntegerField()  # Instead of 'years'

    class Meta:
        db_table = "memberexperience"

    def __str__(self):
        return f"{self.organizationname} - {self.totalmonthexperience} months"


class MemberLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=100) 

    class Meta:
        db_table = "memberlanguage"

    def __str__(self):
        return f"{self.member} - {self.language}"


class MemberLink(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    link_name = models.CharField(max_length=100)
    link_url = models.URLField(max_length=255)

    class Meta:
        db_table = "memberlink"

    def __str__(self):
        return f"{self.member} - {self.link_url}"

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)  # Associate post with user
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    posttitle = models.CharField(max_length=100)
    postcontent = models.FileField(upload_to="content/", blank=True, null=True)  # Store media
    postdesc = models.TextField()  # Caption
    postdttime = models.DateTimeField(auto_now_add=True)  # Auto-set time

    class Meta:
        db_table = "post"

    def __str__(self):
        return f"{self.posttitle} - {self.posttitle}"


'''class Job(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    cmpname = models.CharField(max_length=100)
    position = models.CharField(max_length=100, null = True)
    noofvacancies = models.IntegerField()
    requiredqualification = models.CharField(max_length=100)
    requiredexperience = models.CharField(max_length=100)
    jobdescription = models.CharField(max_length=100)
    jobtype = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    applystartdate = models.DateField()
    lastdate = models.DateField()
    skillsrequired = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "job"'''
class Job(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)  # Optional agency
    cmpname = models.CharField(max_length=100)
    position = models.CharField(max_length=100, null=True)
    noofvacancies = models.IntegerField()
    requiredqualification = models.CharField(max_length=100)
    requiredexperience = models.CharField(max_length=100)
    jobdescription = models.TextField()
    jobtype = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    applystartdate = models.DateField()
    lastdate = models.DateField()
    skillsrequired = models.CharField(max_length=100)
    salary = models.CharField(max_length=255,null=True, blank=True)
    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "job"


class Application(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    applydate = models.DateField()
    status = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100, blank=True)
    attachment = models.FileField(upload_to='resumes/', null=True, blank=True)
    
    class Meta:
        db_table = "application" 

from django.utils import timezone

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    commentsdate = models.DateTimeField(default=timezone.now)
    comments = models.CharField(max_length=100)

    class Meta:
        db_table = "comments"
    
    def __str__(self):
        return f"{self.login} on {self.post}"
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    fromlogin= models.ForeignKey(Login, related_name='messages_sent', on_delete=models.CASCADE)
    tologin = models.ForeignKey(Login, related_name='messages_received', on_delete=models.CASCADE)
    msg = models.CharField(max_length=100)
    msgdt = models.DateField()

    class Meta:
        db_table = "message"

class Likes(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "likes"
        unique_together = ('login', 'post')  # Prevent duplicate likes from same user

class Followers(models.Model):
    id = models.AutoField(primary_key=True)
    followid = models.CharField(max_length=100)
    login = models.ForeignKey(Login, on_delete=models.CASCADE)
    followdate = models.DateField()

    class Meta:
        db_table = "followers"