$(function () {
        $('.cancel_btn').click(function () {
            $('.mymodal').addClass('hide');
            $('.shadow').addClass('hide');
        })

        $('#add_modal').click(function () {
            $('#shadow_window').removeClass('hide');
            $('#modal_window').removeClass('hide');
        })

        $('#add_btn').click(function () {
            $.ajax({
                url:'/modal_add_student/',
                type:'POST',
                dataType:'JSON',
                data:{'stu_name':$('#add_student_name').val(),'class_id':$('#add_class_name').val()},
                success:function (arg) {
                    if(arg.status){
                        location.reload();
                    }else{
                        $('#error_mess_add').text(arg.message);
                    }
                }
            })
        })

        $('.show_editWindow').click(function () {
            $('#shadow_window').removeClass('hide');
            $('#modal_window_edit').removeClass('hide');
            arg = $(this).parent().prevAll();
            stu_id = $(arg[2]).text()
            stu_name = $(arg[1]).text();
            clsid = $(arg[0]).attr('clsid');
            console.log(clsid);
            $('#edit_stu_id').text(stu_id);
            $('#select_class').val(clsid);
            $('#edit_stu_name').val(stu_name);
        })

        $('#edit_btn').click(function () {
            $.ajax({
                url:'/modal_edit_student/',
                type:'POST',
                dataType:'JSON',
                data:{'stu_id':$('#edit_stu_id').text(),'stu_name':$('#edit_stu_name').val(),'class_id':$('#select_class').val()},
                success:function (arg) {
                    if(arg.status){
                        location.reload();
                    }else{
                        $('#edit_erro').text(arg.message);
                    }
                }
            })
        })

        $('.del_maodal_show').click(function (){
            $('#shadow_window').removeClass('hide');
            $('#modal_window_del').removeClass('hide');
            arg = $(this).parent().prevAll();
            class_name=$(arg[0]).text();
            s_name = $(arg[1]).text();
            nid= $(arg[2]).text();
            $('#del_stu_id').text(nid);
            $('#del_stu_name').text(s_name);
            $('#del_class_name').text(class_name);
        })

        $('#del_button').click(function(){
            $.ajax({
                url:'/modal_del_student/',
                type:'POST',
                dataType:'JSON',
                data:{'nid':$('#del_stu_id').text()},
                success:function (arg){
                    if(arg.status){
                        location.href='/student/1.html'
                    }else{
                        $('#del_erro').text(arg.message);
                    }
                }
            })
        })

    })