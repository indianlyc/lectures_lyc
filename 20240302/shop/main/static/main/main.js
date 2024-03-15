function get_and_insert(url) {
const Http = new XMLHttpRequest();
    //const url= //'https://jsonplaceholder.typicode.com/users';
    Http.open("GET", url);
    Http.responseType = 'json';

    Http.onload = (e) => {
      // if (this.readyState == 4 && this.status == 200) {
      const good = document.getElementsByClassName('good-list')[0];
      good.replaceChildren();
      //console.log(Http.response);
      Http.response.forEach(($li) => {
        //console.log($li);
        //console.log(good);
        const newDiv = document.createElement("div");
        // console.log($li);
        const newContent = document.createTextNode($li['title']);
        newDiv.appendChild(newContent);

        const newDiv2 = document.createElement("div");
        // console.log($li);
        const newContent2 = document.createTextNode($li['description']);
        newDiv2.appendChild(newContent2);
        //console.log(newSpan);
        good.appendChild(newDiv);
        good.appendChild(newDiv2);

       });
      // console.log(Http.responseText);
      // }
    };
    Http.send();
};


window.addEventListener("load", () => {
    get_and_insert('/api/search/10000/None');


    document.querySelector('#search-form').addEventListener('submit', (e) => {
        console.log("post");
        e.preventDefault();
        return false;
    });

    document.querySelector('#search-button').addEventListener('click', (e) => {
        console.log("click");
        get_and_insert('/api/search/10000/' + document.getElementById("id_query").value);
        return false;
    });

 });