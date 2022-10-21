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

function DisplayExtra(){
    x = document.getElementById('extra-actions')
    if(x.classList.contains('hidden')){

        x.classList.remove("hidden");
        x.classList.add('additional-actions');
    }else{


        x.classList.remove("additional-actions");
        x.classList.add('hidden');
    }
}