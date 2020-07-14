class Sidebar {
    constructor(sidebar_id, content_id) {
        this.sidebar = document.getElementById(sidebar_id);
        this.contentField = document.getElementById(content_id);
        if (this.sidebar) {
            this.resizer = document.createElement('div');
            this.resizer.className = 'drag-handle';
            this.resizer.style.height = '100%';
            this.sidebar.appendChild(this.resizer);

            this.init_listener = this.initResize.bind(this);
            this.resize_listener = this.Resize.bind(this);
            this.stop_resize_listener = this.stopResize.bind(this);

            this.resizer.addEventListener('mousedown', this.init_listener, false);
        }

    }

    initResize(e) {
        // window.addEventListener('mousemove', this.Resize, false);
        // window.addEventListener('mouseup', this.stopResize, false);

        // window.addEventListener('mousemove', (e, ) => {this.Resize(e)}, false);
        // window.addEventListener('mouseup', (e) => {this.stopResize(e)}, false);

        // console.log(this);

        window.addEventListener("mousemove", this.resize_listener, false);
        window.addEventListener("mouseup", this.stop_resize_listener, false);

        // console.log("should be resizing sidebar");
    }

    Resize(e) {
        this.sidebar.style.width = (e.clientX - this.sidebar.offsetLeft) + 'px';

        // console.log("should be resizing sidebar");
        if (this.contentField !== null){
            this.contentField.style.width = 'calc(100vw - ' + (e.clientX - this.sidebar.offsetLeft) + 'px)';
            // console.log("should be resizing content");
        }

    }

    stopResize(e) {
        window.removeEventListener('mousemove', this.resize_listener, false);
        window.removeEventListener('mouseup', this.stop_resize_listener, false);
    }
}