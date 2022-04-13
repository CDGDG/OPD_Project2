$(document).ready(function(){
    $('#create_comment_btn').click(function(){
        contents = $("#id_comment").val()
        if(contents.trim() == ""){
            $(this).tooltip("show")
            return false;
        }
        else if(contents.length > 200){
            alert('댓글이 너무 길어요.')
            return false;
        }

        $.ajax({
            url: commenturl,
            type: 'POST',
            data: {contents: contents, 'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(), 'private': $('[name=private]').val()},
            dataType: 'json',
            success: function(response){
                if(response['data']=="success"){
                    let pk = response['pk']
                    let who = response['who']
                    let regdate = response['regdate']
                    let contents = response['contents']
                    let nickname = response['nickname']
                    let pic = response['pic']
                    console.log('댓글 작성 성공')
                    $("#id_comment").val('')
                    $('#commentDiv').after(
                        $(`<div class="comment-control rounded p-2 mt-2 div${pk}">
                        <img class="rounded-circle border border-1" style="height:3vw;width:3vw;object-fit: contain;border-color:white !important"
                        src=${pic?pic:"/media/user_icon.png"} alt="이미지 없음">
                        <label class="px-4 d-inline-block rounded p-1 mb-3" style='font-family: "Noto Sans KR", sans-serif; color: white; background-color: lightcoral;'><a class="text-decoration-none text-white" href=${who=='developer'?'{% url "Developer:info" '+pk+' %}':'{% url "Company:detail" '+pk+' %}'}>${nickname}</a></label>
                        <label class="px-4 d-inline-block rounded p-1 mb-3 text-white ${who=='developer'?'bg-primary':'bg-warning'}">${who=='developer'?'개발자':'기업'}</label>
                        <label class="px-4 d-inline-block bg-success rounded p-1 mb-3 text-white">방금</label>
                        <p class="px-1">${contents}</p>
                        <button class="btn btn-danger mb-1 ${pk}">삭제</button>
                        <script>
                        $(".${pk}").click(function(){
                            $.ajax({
                                url: "/board/commentdelete/",
                                type: "POST", 
                                data: {'csrfmiddlewaretoken': $("[name=csrfmiddlewaretoken]").val(), 'pk': '${pk}'},
                                dataType: "json", 
                                success: function(response){
                                        console.log("삭제성공")
                                        $('.div${pk}').slideUp("fast", function(){$(".div${pk}").remove()})
                                }
                            })
                        })
                        </script>
                        </div>`)
                    )
                    
                }
            }
        })
    })
})