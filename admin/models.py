from django.db import models

class Admin(models.Model):
    adminid = models.CharField(max_length=20)
    password = models.TextField()

    class Meta:
        db_table = 'opd_admin'
        verbose_name = '관리자'
        verbose_name_plural = '관리자(들)'

    def __str__(self):
        return self.adminid

class Notice(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    contents = models.TextField()
    regdate = models.DateTimeField(auto_now_add=True)
    viewcnt = models.IntegerField(default=0)

    class Meta:
        db_table = 'opd_notice'
        verbose_name = '공지사항'
        verbose_name_plural = '공지사항(들)'

    def __str__(self):
        return self.title

class NoticeImg(models.Model):
    notice = models.ForeignKey(Notice,on_delete=models.CASCADE)
    img = models.FileField(upload_to='noticeimg_img/')
    img_original = models.TextField(null=False)

    class Meta:
        db_table = 'opd_noticeimg'
        verbose_name = '공지사항 이미지'
        verbose_name_plural = '공지사항 이미지(들)'
        
    def __str__(self):
        return self.notice.title + '의 이미지'
    
class Language(models.Model):
    language = models.CharField(max_length=30)

    class Meta:
        db_table = 'opd_language'
        verbose_name = '언어'
        verbose_name_plural = '언어(들)'

    def __str__(self):
        return self.language


