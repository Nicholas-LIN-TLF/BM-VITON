document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById("sidebar");
    const toggleBtn = document.getElementById("toggleBtn");

    // 点击按钮展开/收起
    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("active");
        // 改变箭头方向
        if (sidebar.classList.contains("active")) {
            toggleBtn.innerHTML = "&#9654;"; // ▶ 向右
        } else {
            toggleBtn.innerHTML = "&#9664;"; // ◀ 向左
        }
    });

    // 点击导航栏以外区域时收起
    document.addEventListener("click", function (event) {
        if (
            sidebar.classList.contains("active") &&
            !sidebar.contains(event.target) &&
            !toggleBtn.contains(event.target)
        ) {
            sidebar.classList.remove("active");
            toggleBtn.innerHTML = "&#9664;";
        }
    });
});
