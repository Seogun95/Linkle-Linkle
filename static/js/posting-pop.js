// ================================= 테스트 완료
function posting() {
    let post_url = $('#postingPop__url').val();
    let post_title = $('#postingPop__title').val();

    $.ajax({
        type: 'POST',
        url: '/posting',
        data: { post_url: post_url, post_title: post_title },
        success: function (response) {
            alert(response);
        },
    });
}

// =================================

function urlPosting() {
    $.ajax({
        type: 'GET',
        url: '/',
        data: {},
        success: function (response) {
            let rows = response[''];
            for (let i = 0; i < rows.length; i++) {
                let temp_html = `
                <
                    <div class="row row-cols-4 row-cols-md-2 g-4" id="cards-box">
                        <div class="col cards-box" data-aos="fade-up" data-aos-delay="200" data-aos-easing="ease-in-out" data-aos-once="false">
                            <div class="cards-box__container logo">
                                <div class="cards-box__card" style="width: 18rem">
                                    <a href="${url}">
                                        <img src="${img}" class="cards-box__img" alt="bookimage" />

                                        <p class="cards-box__body-title">${title}</p>
                                    </a>
                                    <p class="cards-box__body-comment">${comments}</p>
                                    <p class="cards-box__body-user">by. ${user_nickname}</p>
                                </div>
                            </div>
                        </div>
                    </div>
               `;
                $('#').append(temp_html);
            }
        },
    });
}
