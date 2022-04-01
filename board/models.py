from django.db import models
# from developer.models import Developer


class Board(models.Model):
    developer = models.ForeignKey('developer.Developer', on_delete=models.CASCADE, verbose_name='작성자')
    language = models.ForeignKey('admin.Language', on_delete=models.CASCADE, verbose_name='언어', null=True)
    title = models.CharField(max_length=20, verbose_name='제목')
    contents = models.TextField(verbose_name='내용')
    regdate = models.DateField(auto_now_add=True, verbose_name='등록시간')
    viewcnt = models.IntegerField(default=0, verbose_name='조회수')

    class Meta:
        db_table = 'opd_board'
        verbose_name = '게시판'
        verbose_name_plural = '게시판(들)'

    def __str__(self):
        return f'id{self.id}:{self.title}|{self.developer}'

class Boardimg(models.Model):
    board = models.ForeignKey('board.Board', on_delete=models.CASCADE, verbose_name='게시판')
    img = models.FileField(upload_to='boardimg_img/', default="")
    img_original = models.CharField(max_length=200, null=False)

    class Meta:
        db_table = 'opd_boardimg'
        verbose_name = '게시판그림'
        verbose_name_plural = '게시판그림(들)'

    
class Comment(models.Model):
    board = models.ForeignKey('board.Board', on_delete=models.CASCADE, verbose_name='게시판')
    developer = models.ForeignKey('developer.Developer', on_delete=models.CASCADE, verbose_name='작성자')
    contents = models.CharField(max_length=100, verbose_name='댓글내용')
    regdate = models.DateField(auto_now_add=True, verbose_name='등록시간')
    private = models.BooleanField(default=False)


    class Meta:
        db_table = 'opd_comment'
        verbose_name = '댓글'
        verbose_name_plural = '댓글(들)'