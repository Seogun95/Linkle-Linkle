// 카테고리 post 존재시 사라지게 하는 함수
// $(document).ready(function () {});
// let get_list;
// if (!get_list) {
//     $('.category').show();
//     $('.main').hide();
// } else {
//     $('.category').hide();
//     $('.main').show();
// }

// function checking() {
//     $.ajax({
//         type: 'GET',
//         url: '/post',
//         data: {},
//         success: function (response) {
//             let check = response;
//             if (check === null) {
//                 $('.category').show();
//                 $('.main').hide();
//             } else {
//                 $('.category').hide();
//                 $('.main').show();
//             }
//         },
//     });
// }

function category() {
    let img_url = $('#category-img').val();
    let category_name = $('#category-title').val();

    $.ajax({
        type: 'POST',
        url: '/category',
        data: { category_name: category_name, category_img_url: img_url },
        success: function (response) {
            alert(response['msg']);
        },
    });
}
