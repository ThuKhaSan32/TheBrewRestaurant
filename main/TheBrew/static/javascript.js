document.addEventListener('DOMContentLoaded', function (e) {
    e.preventDefault();
    const userId = localStorage.getItem('userId');

    const profile_btn= document.getElementById('profile-btn');
    const noti_btn= document.getElementById('noti_btn');
    const psw_btn= document.getElementById('psw-btn');
    const logout_btn= document.getElementById('logout-btn');
    const promo_btn= document.getElementById('promo_btn');

    if(promo_btn){
        promo_btn.addEventListener('click', function(j){
            j.preventDefault();
            if (userId){
                window.location.href=`/promotions/${userId}`
            } else {
                window.location.href=`/promotions/`
            }
        })
    }

    if(profile_btn){
        profile_btn.addEventListener('click',function(e){
            e.preventDefault();

            if (userId) {
                window.location.href = `/profile/${userId}/`;
            } else {
                alert("You are not logged in");
            }
        });
    }

    if(noti_btn){
        noti_btn.addEventListener('click', function(h) {
            h.preventDefault();

            if (userId) {
                window.location.href = `/notifications/${userId}/`;
            } else {
                alert("You are not logged in");
            }
        });
    }

    if(psw_btn){
        psw_btn.addEventListener('click', function(f) {
            f.preventDefault();

            if (userId) {
                window.location.href = `/edit/${userId}/`;
            } else {
                alert("You are not logged in");
            }
        });
    }

    if(logout_btn){
        logout_btn.addEventListener('click',function(g){
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
    }
})
