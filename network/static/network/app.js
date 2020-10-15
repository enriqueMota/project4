document.addEventListener('DOMContentLoaded', () => {


     const a = document.querySelectorAll('#editing');
     const b = document.querySelectorAll('#edition');
     for (let i = 0; i < a.length; i++) {
          const element = a[i];
          element.style.display = 'none';          
     }
     for (let i = 0; i < b.length; i++) {
          const element = b[i];
          element.style.display = 'none';
     }
     
     if(document.querySelector('.posts')){
          document.querySelector('.posts').addEventListener('click', (event) => {

               
               

               if(event.target.innerHTML === 'Edit'){
                    appear(event.target);
               }else if(event.target.value === 'Update'){
                    disappear(event.target);
                    update(event.target);
                    return false;
               }else if(event.target.className === 'far fa-heart'){

                    let counter = parseInt(event.target.nextSibling.data.slice(-1));
                    const post_id = parseInt(event.target.parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML);

                    counter++;
                    event.target.nextSibling.data = ` ${counter}`;
                    event.target.className = 'fas fa-heart';
                    event.target.style.color = 'red';


                    fetch(`/like/${post_id}`, {
                         method: "POST",
                         headers: {
                              "X-CSRFToken": getCookie("csrftoken"),
                              "Accept": "application/json",
                              "Content-Type": "application/json"},
                         credentials: "same-origin",
                         body: JSON.stringify({
                              post_id: post_id
                         })
                    })
                    .then(response => response.json())
                    .then(data => {
                         console.table(data)
                    })

               }else if(event.target.className === 'fas fa-heart'){

                    let counter = parseInt(event.target.nextSibling.data.slice(-1));
                    const post_id = parseInt(event.target.parentElement.parentElement.firstElementChild.nextElementSibling.innerHTML);

                    counter--;
                    event.target.nextSibling.data = ` ${counter}`;
                    event.target.className = 'far fa-heart';
                    event.target.style.color = '#212529';

                    fetch(`/dislike/${post_id}`, {
                         method: "POST",
                         headers: {
                              "X-CSRFToken": getCookie("csrftoken"),
                              "Accept": "application/json",
                              "Content-Type": "application/json"},
                         credentials: "same-origin",
                         body: JSON.stringify({
                              post_id: post_id
                         })
                    })
                    .then(response => response.json())
                    .then(data => {
                         console.table(data)
                    })
               }
          })

     }     
})

getCookie = (name) => {
     let cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         let cookies = document.cookie.split(';');
         for (let i = 0; i < cookies.length; i++) {
             let cookie = cookies[i].trim();
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) === (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
}

update = (element) => {

     if (element.parentNode.parentNode.children['aydi'] && element.parentNode.children['text']){

          const identity = parseInt(element.parentNode.parentNode.children['aydi'].innerHTML);
          const content  = element.parentNode.children['text'].value;

          fetch('/post', {
               method: "POST",
               credentials: "same-origin",
               headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
               },
               body: JSON.stringify({
                    id: identity,
                    body: content
               })
          })
          .then(response => response.json())
          .then(data => {
               console.table(data)
          })
     }
}

disappear = (element) => {


     const son = element.parentElement;
     const father = son.parentElement;
     
     if('body' in father.children){
          father.children['body'].style.display = 'block';
          father.children['body'].innerHTML = `${son.firstElementChild.value}`;
          father.children['edition'].style.display = 'none';

     }
}

appear = (element) => {
  
     let body = element.nextElementSibling;
     body.style.display = 'none';
     body.nextElementSibling.style.display = 'block'

     // element.nextElementSibling

     // const o = element.parentElement;
     // const a = o.nextElementSibling;
     // a.style.display = 'block';
     // a.style.animationPlayState = 'running';
     // element.querySelector('#edit').parentNode.nextElementSibling.children[0].firstElementChild.value = element.nextElementSibling.innerHTML

 
}

window.onload = () => {

     if(document.querySelector('#follow')){

          document.querySelector('#follow').onclick = () => {
     
               let contador = parseInt(document.querySelector('#asyc').innerHTML.slice(-1));
               const username = document.querySelector('#strong').innerHTML;
               
               if(document.querySelector('#follow').innerHTML === 'Follow'){
                    
                    document.querySelector('#follow').innerHTML = 'Unfollow';
                    contador++;
                    document.querySelector('#asyc').innerHTML = `Followers: ${contador}`;

                    fetch(`/follow/${username}`, {
                         method: "POST",
                         headers: {
                              "X-CSRFToken": getCookie("csrftoken"),
                              "Accept": "application/json",
                              "Content-Type": "application/json"},
                         credentials: "same-origin",
                         body: JSON.stringify({
                              username: username
                         })
                    })
                    .then(response => response.json())
                    .then(data => {
                         console.table(data)
                    })


               }else{
                    document.querySelector('#follow').innerHTML = 'Follow';
                    contador--;
                    document.querySelector('#asyc').innerHTML = `Followers: ${contador}`;

                    fetch(`/unfollow/${username}`, {
                         method: "POST",
                         headers: {
                              "X-CSRFToken": getCookie("csrftoken"),
                              "Accept": "application/json",
                              "Content-Type": "application/json"},
                         credentials: "same-origin",
                         body: JSON.stringify({
                              username: username
                         })
                    })
                    .then(response => response.json())
                    .then(data => {
                         console.table(data)
                    })

               }
          }
     }
}

