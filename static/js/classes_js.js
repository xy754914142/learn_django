$(function () {
        $('.cancel_btn').click(function () {
            $('.mymodal').addClass('hide');
            $('.shadow').addClass('hide');
        })

        $('#show_add').click(function () {
            $('#add_modal').removeClass('hide');
            $('.shadow').removeClass('hide');
        })
        $('#add_submit').click(function () {
            $.ajax({
                url:'/modal_add_class/',
                type:'POST',
                data:{'class_name':$('#class_name').val()},
                dataType:"JSON",
                success:function (args) {
                    if(args.status){
                        location.reload();
                    }else{
                        $('#error_msg').text(args.message);
                    }
                }
            })
        })

        $('.show_edit').click(function () {
            $('#edit_modal').removeClass('hide');
            $('#shadow').removeClass('hide');
            p_all = $(this).parent().prevAll()
            nid = $(p_all[1]).text();
            class_name = $(p_all[0]).text();
            $('#nid').text(nid);
            $('#edit_class_name').val(class_name);
        })
        $('#change_submit').click(function () {
            $.ajax({
                url:'/modal_edit_class/',
                type:'POST',
                dataType:'JSON',
                data:{'nid':$('#nid').text(),'class_name':$('#edit_class_name').val()},
                success:function (arg) {
                    if(arg.status){
                        location.reload();
                    }else{
                        $('#error_msg_edit').text(arg.message);
                    }
                }
            })
        })

        $('.show_del').click(function () {
            $('#shadow').removeClass('hide');
            $('#del_modal').removeClass('hide');
            c_all = $(this).parent().prevAll();
            $('#del_id').text($(c_all[1]).text())
            str_class = '是否删除名为：'+$( c_all[0]).text() +'的班级'
            $('#del_name').text(str_class)
        })
        $('#del_btn').click(function () {
            $.ajax({
                url:'/modal_del_class/',
                type:'POST',
                dataType:'JSON',
                data:{'nid':$('#del_id').text()},
                success:function (arg) {
                    if(arg.status){
                        location.reload();
                    }else{
                        $('#error_msg_del').val(arg.message);
                    }
                }
            })
        })
    })