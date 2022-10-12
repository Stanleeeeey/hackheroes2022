//js for index.html
//main coder Stanislaw Kawulok

function ShowMenu(){
    x = document.getElementById('hidden-menu');

    if(x.classList.contains('hidden-menu')){

        x.classList.remove("hidden-menu");
        x.classList.add('visible-menu');
    }else{


        x.classList.remove("visible-menu");
        x.classList.add('hidden-menu');
    }
    
}