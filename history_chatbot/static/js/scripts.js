/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

document.addEventListener('DOMContentLoaded', function() {
    // Lấy danh sách các mục trong mục lục
    const tocItems = document.querySelectorAll('#toc .nav-link');
    // Lặp qua từng mục trong mục lục và gắn sự kiện cuộn
    tocItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault(); // Ngăn chặn hành vi mặc định của thẻ a

            // Lấy ID của phần nội dung tương ứng với mục mục lục được nhấp
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);    
            console.log(targetId)
            // Cuộn trang đến phần nội dung tương ứng
            if (targetElement) {
                console.log("---"+targetElement)
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // document.getElementById('content').addEventListener('scroll', function() {
    //     // Lấy vị trí hiện tại của thanh cuộn
    //     const scrollPosition = this.scrollTop;

    //     // Lấy tất cả các mục mục lục
    //     const tocItems = document.querySelectorAll('#toc .nav-item a');
        
    //     // Lặp qua từng phần tử nội dung và kiểm tra xem nó có nằm trong vùng nhìn thấy không
    //     document.querySelectorAll('#content > h4, #content > h5, #content > h6').forEach(function(section) {
    //         const sectionTop = section.offsetTop;
    //         const sectionHeight = section.offsetHeight;

    //         if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
    //             // Lấy ID của phần tử nội dung hiện tại
    //             const sectionId = section.getAttribute('id');

    //             // Làm cho mục mục lục tương ứng được in đậm
    //             const activeTocItem = document.querySelector(`#toc .nav-item a[href="#${sectionId}"]`);
    //             if (activeTocItem) {
    //                 // Xóa lớp 'active' từ tất cả các mục mục lục
    //                 tocItems.forEach(function(item) {
    //                     item.classList.remove('active');
    //                 });
    //                 // Thêm lớp 'active' cho mục mục lục tương ứng
    //                 activeTocItem.classList.add('active');
    //             }
    //         }
    //     });
    // });
});

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.add('navbar-shrink')
            // navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});
