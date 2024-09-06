function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    // Add To Selection
    $(".add-to-selection").on("click", function(){
        let button = $(this)
        let id = button.attr("data-index")

        let hotel_id = $("#id").val()
        let room_id = $(`.room_id_${id}`).val()
        let room_number = $(`.room_number_${id}`).val()
        let hotel_name = $("#hotel_name").val()
        let room_name = $("#room_name").val()
        let room_price = $("#room_price").val()
        let number_of_beds = $("#number_of_beds").val()
        let room_type = $("#room_type").val()
        let checkin = $("#checkin").val()
        let checkout = $("#checkout").val()
        let adult = $("#adult").val()
        let children = $("#children").val()

        // console.log(`${id} Added To Selection`);
        console.log( hotel_id);
        console.log(room_number);
        console.log(room_id);
        console.log(hotel_name);
        console.log(room_name);
        console.log(room_price);
        console.log(number_of_beds);
        console.log( room_type);
        console.log(checkin);
        console.log(checkout);
        console.log(adult);
        console.log(children);

        $.ajax({
            url:'/booking/add_to_selection/',
            // method: 'POST',
            data: {
                'id': id,
                'hotel_id': hotel_id,
                'room_id': room_id,
                'room_number': room_number,
                'hotel_name': hotel_name,
                'room_name': room_name,
                'room_price': room_price,
                'number_of_beds': number_of_beds,
                'room_type': room_type,
                'checkin': checkin,
                'checkout': checkout,
                'adult': adult,
                'children': children,
            },
            dataType: 'json',
            beforeSend: function(){
                console.log("Sending data to server...");
                
                button.html("<i class='fas fa-spinner fa-spin'></i> Processing... ")
            },
            success: function(response){
                console.log(response);
                $(".room-count").text(response.total_selected_items);
                button.html("<i class= 'fas fa-check'></>Added To Selection")

            }
            
        })
    })

})

// Delete Items from cart
$(document).on('click', '.delete-item', function() {
    let id = $(this).attr('data-item');
    let button = $(this);
    
    Swal.fire({
        title: "Are you sure you want to delete this room?",
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: '/booking/delete_selection/',
                data: {
                    'id': id,
                },
                dataType: 'json',
                beforeSend: function() {
                    button.html("<i class='fas fa-spinner fa-spin'></i>");
                },
                success: function(res) {
                    console.log(res.total_selected_items);
                    $(".room-count").text(res.total_selected_items);
                    $(".selection-list").html(res.data);
                    Swal.fire(
                        'Deleted!',
                        'The room has been deleted.',
                        'success'
                    );
                },
                error: function() {
                    Swal.fire(
                        'Error!',
                        'There was a problem deleting the room.',
                        'error'
                    );
                    button.html("Delete"); // Reset button text
                }
            });
        }
    });
});
// $(document).on('click','.delete-item',function() {
//     let id = $(this).attr('data-item');
//     // console.log(id)
//     let button = $(this);

//     Swal.fire({
//         title: "Are you sure you want to delete this room?",
//         text: "You won't be able to revert this!",
//         icon: "warning",
//         showCancelButton: true,
//         confirmButtonColor: "#3085d6",
//         cancelButtonColor: "#d33",
//         confirmButtonText: "Yes, delete it!"
//     }).then(result) => {
//         if (result.isConfirmed) {
//             $.ajax({
//                 url:'/booking/delete_selection/',
//                 data:{
//                     'id':id,
//                 },
//                 dataType:'json',
//                 beforeSend:function(){
//                     button.html("<i class='fas fa-spinner fa-spin'></i>");
//                 },
//                 success:function(res){
//                     console.log(res.total_selected_item)
//                     $(".room-count").text(res.total_selected_items);
//                     $(".selection-list").html(res.data);
//                 },  
//             });
//         }
//     };
// });    

    


function makeAjaxCall() {
    $.ajax({
        url: '/update_room_status/',  
        type: 'GET',
        success: function(data) {
            console.log("Checked Rooms");
        },
    });
}

setInterval(makeAjaxCall, 3000);



// Add to bookmark

// makeAjaxCall();

// $(document).on('change', '#noti-status', function(){
//     const query = $(this).val()
    
//     $.ajax({
//         url:"/dashboard/notification_filter/",
//         beforeSend: function(){
//             console.log("Sending Data...");
//         },
//         data: {
//             "query": query
//         },
//         success: function(res){
//             console.log(res.data);
//             $(".noti-div-main").html(res.data);

//         }
//     })
// })