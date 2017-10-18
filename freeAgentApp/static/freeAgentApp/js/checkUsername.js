$(function(){
    var username = $('.id_username').val();
    var $pTag = document.getElementById('pTag-username');

    function exist() {
        $pTag.innerHTML = 'User Name existed!'
    }

    $.ajax({
        type:'get',
        url:'freeAgentApp/serializerUsername',
        dataType:'json',
        success: function (user) {
            for(var i = 0; i < user.length; i++){
                if (user[i].username = username){
                    exist();
                    break;
                }
            }
        }
    })  
});
