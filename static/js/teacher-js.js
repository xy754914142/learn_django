$(function () {
    BindCancel();
    Bindshow_add_modal();
    Bindadd_btu();
    Bindshow_edit_modal();
    Bindedit_btu();
    Bindshow_del_modal();
    Binddel_btn();
})


function BindCancel() {
    $('.cancel').click(function () {
        $('.shadow,.mymodal').addClass('hide');
    })
}
function Bindshow_add_modal() {
    $('#show_add_modal').click(function () {
        $('.shadow,.loading').removeClass('hide');
        $.ajax({
            url:'/get_class_list/',
            type:'GET',
            dataType:'JSON',
            success:function (arg) {
                $.each(arg,function (i,row) {
                    var tag = document.createElement('option');
                    tag.innerHTML = row.class_name;
                    tag.setAttribute('value',row.id);
                    $('#add_select').append(tag);
                })
                $('.loading').addClass('hide');
                $('#add_modal').removeClass('hide');
            }
        })
    })
}
function Bindadd_btu() {
    $('#add_btu').click(function () {
        $.ajax({
            url:'/modal_add_teacher/',
            type:'POST',
            dataType:'JSON',
            data:{'t_name':$('#add_t_name').val(),'class_id_list':$('#add_select').val()},
            traditional:true,
            success:function (arg) {
                if(arg.status){
                    location.reload();
                }else{
                    $('#add_err').text(arg.message);
                }
            }
        })
    })
}
function Bindshow_edit_modal() {
    $('.show_edit_modal').click(function () {
        $('.shadow,.loading').removeClass('hide')
        arg = $(this).parent().prevAll()
        nid = $(arg[2]).text();
        t_name = $(arg[1]).text();
        $('#edit_t_name').val(t_name);
        $('#edit_id').text(nid);
        $('#edit_select').find('option').remove();
        $.ajax({
            url: '/get_teacher2class_list/',
            type: 'POST',
            dataType: 'JSON',
            data: {'nid': nid},
            success: function (arg) {
                 $.ajax({
                        url:'/get_class_list/',
                        type:'GET',
                        dataType:'JSON',
                        success:function (value) {
                            $.each(value,function (i,row) {
                                var tag = document.createElement('option');
                                tag.innerHTML = row.class_name;
                                tag.setAttribute('value',row.id);
                                if(arg.indexOf(row.id) != -1){
                                    tag.setAttribute('selected','selected');
                                }
                                $('#edit_select').append(tag);
                            })
                            $('.loading').addClass('hide');
                            $('#edit_modal').removeClass('hide');
                        }
                    });
            }
        })


    })

}
function Bindedit_btu() {
    $('#edit_btu').click(function () {
        $.ajax({
            url:'/modal_edit_teacher/',
            type:'POST',
            dataType:'JSON',
            data:{'nid':$('#edit_id').text(),'t_name':$('#edit_t_name').val(),'class_list':$('#edit_select').val()},
            traditional:true,
            success:function (arg) {
                if(arg.status){
                    location.reload();
                }else{
                    $('#edit_err').text(arg.message);
                }
            }
        })
    })
}
function Bindshow_del_modal() {
    $('.show_del_modal').click(function () {
        $(".shadow,.loading").removeClass('hide');
        arg = $(this).parent().prevAll();
        nid = $(arg[2]).text();
        t_name = $(arg[1]).text();
        class_list = $(arg[0]).text();
        $('#del_id').text(nid);
        $('#del_name').text(t_name);
        $('#del_t_class').text(class_list);
        $(".loading").addClass('hide');
        $('#del_modal').removeClass('hide');
    })

}
function Binddel_btn() {
    $('#del_btn').click(function () {
        $.ajax({
            url:'/modal_del_teacher/',
            type:'POST',
            dataType:'JSON',
            data:{'nid':$('#del_id').text()},
            success:function (arg) {
                if(arg.status){
                    location.reload();
                }else{
                    $('#err_del').text(arg.message);
                }
            }

        })
    })
}