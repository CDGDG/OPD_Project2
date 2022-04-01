from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name='프로젝트 타이틀')
    summary = models.CharField(max_length=100, verbose_name='프로젝트 요약')
    contents = models.TextField(verbose_name='프로젝트 내용')
    startdate = models.DateTimeField(null=True)
    enddate = models.DateTimeField(null=True)
    viewcnt = models.IntegerField(default=0)
    private = models.BooleanField(default=False)
    thumbnail = models.FileField(upload_to='project_thumbnail/')
    thumbnail_original = models.TextField(null=False)

    member = models.ManyToManyField('developer.Developer')
    language = models.ManyToManyField('admin.Language')

    class Meta:
        db_table = 'opd_project'
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트(들)'

    def __str__(self):
        return self.title

class Recruit(models.Model):
    project = models.OneToOneField(
        'project.Project',
        on_delete=models.CASCADE,
        primary_key=True,
    )

    title = models.CharField(max_length=50, verbose_name='모집 타이틀')
    contents = models.TextField(verbose_name='모집 내용')
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='모집 등록일')
    viewcnt = models.IntegerField(default=0, verbose_name='조회수')
    ing = models.BooleanField(default=False, verbose_name='모집 여부')

    class Meta:
        db_table = 'opd_recruit'
        verbose_name = '프로젝트 모집'
        verbose_name_plural = '프로젝트 모집(들)'

    def __str__(self):
        return self.title
    
class RecruitOk(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE)
    developer = models.ForeignKey('developer.Developer', on_delete=models.CASCADE)
    contents = models.TextField()

    class Meta:
        db_table = 'opd_recruitok'
        verbose_name = '프로젝트 모집처리'
        verbose_name_plural = '프로젝트 모집(들)'

    def __str__(self):
        return self.developer.userid + "|" + self.project.title
    
class Recruit_Language(models.Model):
    recruit = models.ForeignKey('project.Recruit', on_delete=models.CASCADE, null=True)
    language = models.ForeignKey('admin.Language', on_delete=models.CASCADE, null=True)
    people = models.IntegerField()

    class Meta:
        db_table = 'opd_recruit_language'
        verbose_name = '프로젝트 모집 언어'
        verbose_name_plural = '프로젝트 모집 언어(들)'

class Document(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트')
    category = models.CharField(max_length=20, verbose_name='문서 카테고리')
    docfile = models.FileField(upload_to='document_docfile/')
    docfile_original = models.TextField(null=False)

    class Meta:
        db_table = 'opd_document'
        verbose_name = '프로젝트 문서'
        verbose_name_plural = '프로젝트 문서(들)'

    def __str__(self):
        return self.project.title + '의 문서'

        
    
    


