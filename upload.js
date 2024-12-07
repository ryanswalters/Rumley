function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const uploadStatus = document.getElementById('uploadStatus');

    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Simulate file upload
        setTimeout(() => {
            uploadStatus.innerText = `File "${file.name}" uploaded successfully.`;
        }, 1000);
    } else {
        uploadStatus.innerText = 'Please select a file to upload.';
    }
}