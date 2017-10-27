window.onload = function () {

    var username = document.getElementById('id_username');
    var input;
    var $pTag = document.getElementById('pTag-Username');

    function check(username){
        $.ajax({
            type:'get',
            url:'../../freeAgentApp/serializerUsername',
            dataType:'json',
            success: function (user) {
                // console.log(user); // test
                for(var i = 0; i < user.length; i++){

                    if (user[i].username == username){
                        exist();
                    }
                }
            }
        })
    }

    function exist() {
        $pTag.innerHTML = 'User Name Exists!'
    }

    username.addEventListener("input",function () {
        input = username.value ;
    })

    username.addEventListener("blur", function () {
        if(input == undefined){

        }else{
            check(input);
            //document.getElementById('pTag-Username').innerHTML = input;
        }
        username.addEventListener("click",function () {
            document.getElementById('pTag-Username').innerHTML = "";
        })
    })

}