//当页面加载完的时候执行

$(function () {
    //初始化顶部轮播图
    initTopSwiper()

    // 初始化mustbuy轮播图
    initMustBuySwiper()
})

//顶部轮播图驱动
function initTopSwiper() {
    var mySwiper = new Swiper ('#topSwiper', {
    autoplay:5000,
    loop: true,

    // 如果需要分页器
    pagination: '.swiper-pagination',

  })
}

function initMustBuySwiper() {
    var swiper = new Swiper('#swiperMenu', {
        // pagination: '.swiper-pagination',
        slidesPerView: 3,
        // paginationClickable: true,
        spaceBetween: 10
    });
}















