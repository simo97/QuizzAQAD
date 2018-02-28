$(document).ready(function(){
    function add_categorie(){
        $.post(add_url, {name : $('#name_input').val()}, function(data){
            if(data.status == 0){
                alert('Categorie created with success');
            }
        })
    }

})