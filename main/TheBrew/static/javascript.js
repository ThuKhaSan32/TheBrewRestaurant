document.addEventListener('DOMContentLoaded', function (e) {
    e.preventDefault();
    const userId = localStorage.getItem('userId');
    document.getElementById('profile-btn').addEventListener('click',function(e){
        e.preventDefault();

        if (userId) {
            window.location.href = `/profile/${userId}/`;
        } else {
            alert("User ID not found in localStorage.");
        }
    });
    document.getElementById('psw-btn').addEventListener('click', function(f) {
        f.preventDefault();

        if (userId) {
            window.location.href = `/edit/${userId}/`;
        } else {
            alert("User ID not found in localStorage.");
        }
    });
    document.getElementById('logout-btn').addEventListener('click',function(g){
        g.preventDefault();

        if(userId){
            fetch(`/logout/${userId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
            }).then(response => response.json()) // parse JSON response
            .then(data => {
                if (data.success) {
                    localStorage.removeItem('userId');
                    localStorage.clear();
                    alert("Logout successful.");
                    window.location.href = '/';
                } else {
                    alert("Logout failed. Please try again.");
                }
            })
            .catch(error => {
                console.error('Error during logout:', error);
                alert("An error occurred while logging out. Please try again.");
            });
        }
        else{
            alert("User ID not found in localStorage.");
            window.location.href = '/';
        }

    })

    document.getElementById('pr-btn')
})
