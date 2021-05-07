// 업로드 사진 미리보기
function cnn_process()
{
		
	var form = $('#FORM')[0];
	var formData = new FormData(form);
	formData.append("file", $("#file")[0].files[0]);	
	
	$.ajax({
	    url: '/cnn_process',
			processData: false,
			contentType: false,
			data: formData,
			type: 'POST',
			dataType:"json",
			success: function(result){
				var color = result["color"]
				var cloth = result["cloth"]
				var color_form = document.getElementById("color");
				color_form[color].selected = true;
				var category_form = document.getElementById("category");
				category_form[cloth].selected = true;
				console.log(result);
				}
	  });
  }
  function cosine_process()
  {
		  
	  var form = $('#FORM')[0];
	  var formData = new FormData(form);
	  var category = $("#category option:selected").val();
	  formData.append("file", $("#file")[0].files[0]);	
	  formData.append("category", category);
	  
	  $.ajax({
		  url: '/cosine_process',
			  processData: false,
			  contentType: false,
			  data: formData,
			  type: 'POST',
			  dataType:"json",
			  success: function(result){
				  result.innerHTML =
				  $("#result_price").html(
					"<br>"+
					"<span style='color:green; font-weight:bold'>평균가: " + result["mean"] + "</span><br>" +
					"<span style='color:red; font-weight:bold'> 최대가: " + result["max"] + "</span>" +
					"<span style='color:blue; font-weight:bold'> 최저가: " + result["min"] + "</span>");
					$("#result_price_img").html(
						"<div class='image_sample'><img src='." + result["img1"] + "'></div>"+
						"<div class='image_sample'><img src='." + result["img2"] + "'></div>"+
						"<div class='image_sample'><img src='." + result["img3"] + "'></div>");
				  console.log(result);
				  }
		});
	}
// 업로드 사진 미리보기
function rnn_process()
{
	var category = $("#category option:selected").val();

	var postdata = {
		"category":category
	}
	
	$.ajax({
	    url: '/rnn_process',
			processData: false,
			contentType: "application/json",
			data: JSON.stringify(postdata),
			type: 'POST',
			dataType:"JSON",
			success: function(result){
				console.log(result);
				document.getElementById("contents").value = result["text"];
				}
	  });
  }

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function (e) {
      $('#preImage').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
  }
}
$("#file").change(function() {
  readURL(this);
});


// 메뉴토글 설정하기
document.addEventListener('DOMContentLoaded', function(){
	document.querySelector(".mobile-menu").addEventListener("click", function(e){
		if ( document.querySelector('.menuwrap').classList.contains('on') ){
				//메뉴닫힘
				document.querySelector('.menuwrap').classList.remove('on');
				document.querySelector('.mobile-menu i').classList.remove('fa-times')
				document.querySelector('.mobile-menu i').classList.add('fa-bars');

				//페이지 스크롤 락 해제
				document.querySelector('#dimmed').remove();
		} else {
				//메뉴펼침
				document.querySelector('.menuwrap').classList.add('on');
				document.querySelector('.mobile-menu i').classList.remove('fa-bars');
				document.querySelector('.mobile-menu i').classList.add('fa-times');

				//페이지 스크롤 락 레이어 추가
				let div = document.createElement('div');
				div.id = 'dimmed';
				document.body.append(div);

				//페이지 스크롤 락  모바일 이벤트 차단
				document.querySelector('#dimmed').addEventListener('scroll touchmove touchend mousewheel', function(e){
						e.preventDefault();
						e.stopPropagation();
						return false;
				});

				//페이지 스크롤 락 레이어 클릭 메뉴 닫기
				document.querySelector('#dimmed').addEventListener('click', function(e){
						document.querySelector(".mobile-menu").click();
				});             

			}
	});
});
