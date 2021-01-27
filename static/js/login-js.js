$(function () {
    Bindinput();

})

function Bindinput() {
    $('#username').blur(function () {
        if($('#username').val().length == 0){
            $('#user_div').addClass('has-error has-feedback');
            var tag = document.createElement('span');
            tag.classList.add('glyphicon', 'glyphicon-remove', 'form-control-feedback');
            tag.setAttribute('aria-hidden',"true");
            $('#user_div_on').append(tag);
        }else{
            $('#user_div').removeClass('has-error','has-feedback');
            $('#user_div').find('span').remove();
            $('#user_div').addClass('has-success has-feedback');
            var tag = document.createElement('span');
            tag.classList.add('glyphicon', 'glyphicon-ok', 'form-control-feedback');
            tag.setAttribute('aria-hidden',"true");
            $('#user_div_on').append(tag);
        }
    });
    $('#password').blur(function () {
        if($('#password').val().length == 0){
            $('#psw_div').addClass('has-error has-feedback');
            var tag = document.createElement('span');
            tag.classList.add('glyphicon', 'glyphicon-remove', 'form-control-feedback');
            tag.setAttribute('aria-hidden',"true");
            $('#psw_div_on').append(tag);
        }else{
            $('#psw_div').removeClass('has-error','has-feedback');
            $('#psw_div').find('span').remove();
            $('#psw_div').addClass('has-success has-feedback');
            var tag = document.createElement('span');
            tag.classList.add('glyphicon', 'glyphicon-ok', 'form-control-feedback');
            tag.setAttribute('aria-hidden',"true");
            $('#psw_div_on').append(tag);
        }
    })
}


