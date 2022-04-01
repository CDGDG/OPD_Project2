from django.db import models

# from project.models import Language, Project

class Company(models.Model):
    companyid = models.CharField(max_length=20, verbose_name='회사아이디')
    password = models.CharField(max_length=50, verbose_name='회사비밀번호')
    name = models.CharField(max_length=15, verbose_name='회사이름')
    pic = models.FileField(upload_to="company_pic/", verbose_name='회사프로필사진')
    pic_original = models.CharField(max_length=200, null=False, verbose_name='회사프로필사진이름')
    tel = models.CharField(max_length=11, verbose_name='회사전화번호')
    email = models.EmailField(max_length=128, verbose_name='회사이메일')
    address = models.CharField(max_length=30, verbose_name='회사주소')
    address_detail = models.CharField(max_length=100, verbose_name='회사상세주소')
    summary = models.TextField(verbose_name='회사설명')
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='가입시간')
    url = models.TextField(verbose_name='회사홈페이지URL')
    people = models.PositiveIntegerField(verbose_name='직원수')
    category = models.CharField(max_length=10, verbose_name='분류')

    likeproject = models.ManyToManyField('project.Project', verbose_name='좋아요한 프로젝트')

    language = models.ManyToManyField('admin.Language', verbose_name='사용언어')

    class Meta:
        db_table = 'opd_company'
        verbose_name = '회사'  # 모델 이름 (admin)
        verbose_name_plural = '회사(들)'  # 모델 복수형 이름 (admin)

    def __str__(self):
        return f'id{self.id}:{self.name}-{self.category}'
