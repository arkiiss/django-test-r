document.addEventListener('DOMContentLoaded',function(){
    async function getCSRFToken() {
        await fetch('',{method: 'GET', credentials: 'same-origin'});
    }
    getCSRFToken();

    const form = document.getElementById('loginForm');
    form.addEventListener('submit',async function (e) {
        e.preventDefault();

        const data = new FormData(form);

        const response = await fetch('',{
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': document.cookie.split('; ').find(row=> row.startsWith('csrftoken='))?.split('=')[1]|| ''
            }
        });
        
        const result = await response.json();
        document.getElementById('result').innerText = JSON.stringify(result);
    });;
});