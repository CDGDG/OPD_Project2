from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=50, verbose_name='프로젝트 타이틀*')
    summary = models.CharField(max_length=100, verbose_name='프로젝트 요약*')
    contents = models.TextField(verbose_name='프로젝트 내용*')
    startdate = models.DateTimeField(null=True)
    enddate = models.DateTimeField(null=True)
    viewcnt = models.IntegerField(default=0)
    private = models.BooleanField(default=False, verbose_name='공개')
    thumbnail = models.FileField(upload_to='project_thumbnail/', null=True)
    thumbnail_original = models.TextField(null=True)

    leader = models.ForeignKey('developer.Developer', on_delete=models.CASCADE, verbose_name='팀장', related_name='%(class)s_leader')

    member = models.ManyToManyField('developer.Developer',related_name='%(class)s_member')
    language = models.ManyToManyField('admin.Language')

    class Meta:
        db_table = 'opd_project'
        verbose_name = '프로젝트'
        verbose_name_plural = '프로젝트(들)'

    def __str__(self):
        return self.title

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

class ProjectComment(models.Model):
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, verbose_name='프로젝트 댓글')
    developer = models.ForeignKey('developer.Developer', on_delete=models.CASCADE, verbose_name="작성자", null=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, verbose_name="작성자", null=True)
    parentComment = models.OneToOneField('project.ProjectComment', on_delete=models.CASCADE, verbose_name='상위 댓글', null=True)
    contents = models.CharField(max_length=200, verbose_name='댓글 내용')
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='댓글 등록일')

    class Meta:
        db_table = 'opd_project_comment'
        verbose_name = '프로젝트 댓글'
        verbose_name_plural = '프로젝트 댓글(들)'

    
    


