document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("download-form");
    const urlInput = document.getElementById("tiktok-url");
    const resultDiv = document.getElementById("result");
    const loadingBar = document.getElementById("loading-bar");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        resultDiv.textContent = "Memproses...";
        loadingBar.style.display = "block";

        const url = urlInput.value.trim();
        if (!url) {
            resultDiv.textContent = "URL tidak boleh kosong.";
            loadingBar.style.display = "none";
            return;
        }

        const formData = new FormData();
        formData.append("url", url);

        fetch("http://localhost:5000/download", {
            method: "POST",
            body: formData
        })
        .then(async response => {
            loadingBar.style.display = "none";
            if (response.ok && response.headers.get("Content-Type").includes("video/mp4")) {
                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = downloadUrl;
                a.download = "tiktok_video.mp4";
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);
                resultDiv.textContent = "Berhasil! File sedang diunduh.";
            } else {
                const data = await response.json();
                resultDiv.textContent = data.error || "Gagal mengunduh video.";
            }
        })
        .catch(() => {
            loadingBar.style.display = "none";
            resultDiv.textContent = "Terjadi kesalahan koneksi ke server.";
        });
    });
});