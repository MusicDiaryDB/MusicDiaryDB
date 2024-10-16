document.addEventListener("DOMContentLoaded", function () {
  // Diary Entry Management
  const createEntryForm = document.getElementById("create-entry-form");
  const updateEntryForm = document.getElementById("update-entry-form");
  const deleteEntryForm = document.getElementById("delete-entry-form");
  const entryOutput = document.getElementById("entry-output");

  // Create Entry
  createEntryForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createEntryForm);
    const response = await fetch("/entry/", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    entryOutput.innerHTML = `<p>${result.message}</p><p>EntryID: ${result.EntryID}</p>`;
  });

  // Update Entry
  updateEntryForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateEntryForm);
    const entryId = formData.get("entryId");
    const response = await fetch(`/entry/${entryId}`, {
      method: "PUT",
      body: formData,
    });
    const result = await response.json();
    entryOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Entry
  deleteEntryForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteEntryForm);
    const entryId = formData.get("entryId");
    const response = await fetch(`/entry/${entryId}`, {
      method: "DELETE",
    });
    const result = await response.json();
    entryOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Diary Report Management
  const createReportForm = document.getElementById("create-report-form");
  const updateReportForm = document.getElementById("update-report-form");
  const deleteReportForm = document.getElementById("delete-report-form");
  const reportOutput = document.getElementById("report-output");

  // Create Report
  createReportForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createReportForm);
    const response = await fetch("/report/", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    reportOutput.innerHTML = `<p>${result.message}</p><p>ReportID: ${result.ReportID}</p>`;
  });

  // Update Report
  updateReportForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateReportForm);
    const reportId = formData.get("reportId");
    const response = await fetch(`/report/${reportId}`, {
      method: "PUT",
      body: formData,
    });
    const result = await response.json();
    reportOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Report
  deleteReportForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteReportForm);
    const reportId = formData.get("reportId");
    const response = await fetch(`/report/${reportId}`, {
      method: "DELETE",
    });
    const result = await response.json();
    reportOutput.innerHTML = `<p>${result.message}</p>`;
  });
  // User Management
  const createUserForm = document.getElementById("create-user-form");
  const updateUserForm = document.getElementById("update-user-form");
  const deleteUserForm = document.getElementById("delete-user-form");
  const userOutput = document.getElementById("user-output");

  // Create User
  createUserForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createUserForm);
    const response = await fetch("/user/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    userOutput.innerHTML = `<p>${result.message}</p><p>UserID: ${result.UserID}</p>`;
  });

  // Update User
  updateUserForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateUserForm);
    const userId = formData.get("userId");
    const response = await fetch(`/user/${userId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    userOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete User
  deleteUserForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteUserForm);
    const userId = formData.get("userId");
    const response = await fetch(`/user/${userId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    userOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Song Management
  const createSongForm = document.getElementById("create-song-form");
  const updateSongForm = document.getElementById("update-song-form");
  const deleteSongForm = document.getElementById("delete-song-form");
  const songOutput = document.getElementById("song-output");

  // Create Song
  createSongForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createSongForm);
    const response = await fetch("/song/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    songOutput.innerHTML = `<p>${result.message}</p><p>SongID: ${result.SongID}</p>`;
  });

  // Update Song
  updateSongForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateSongForm);
    const songId = formData.get("songId");
    const response = await fetch(`/song/${songId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    songOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Song
  deleteSongForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteSongForm);
    const songId = formData.get("songId");
    const response = await fetch(`/song/${songId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    songOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Streaming Platform Management
  const createPlatformForm = document.getElementById("create-platform-form");
  const updatePlatformForm = document.getElementById("update-platform-form");
  const deletePlatformForm = document.getElementById("delete-platform-form");
  const platformOutput = document.getElementById("platform-output");

  // Create Streaming Platform
  createPlatformForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createPlatformForm);
    const response = await fetch("/platform/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    platformOutput.innerHTML = `<p>${result.message}</p><p>PlatformID: ${result.PlatformID}</p>`;
  });

  // Update Streaming Platform
  updatePlatformForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updatePlatformForm);
    const platformId = formData.get("platformId");
    const response = await fetch(`/platform/${platformId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    platformOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Streaming Platform
  deletePlatformForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deletePlatformForm);
    const platformId = formData.get("platformId");
    const response = await fetch(`/platform/${platformId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    platformOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Album Management
  const createAlbumForm = document.getElementById("create-album-form");
  const updateAlbumForm = document.getElementById("update-album-form");
  const deleteAlbumForm = document.getElementById("delete-album-form");
  const albumOutput = document.getElementById("album-output");

  // Create Album
  createAlbumForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createAlbumForm);
    const response = await fetch("/album/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    albumOutput.innerHTML = `<p>${result.message}</p><p>AlbumID: ${result.AlbumID}</p>`;
  });

  // Update Album
  updateAlbumForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateAlbumForm);
    const albumId = formData.get("albumId");
    const response = await fetch(`/album/${albumId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    albumOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Album
  deleteAlbumForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteAlbumForm);
    const albumId = formData.get("albumId");
    const response = await fetch(`/album/${albumId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    albumOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Artist Management
  const createArtistForm = document.getElementById("create-artist-form");
  const updateArtistForm = document.getElementById("update-artist-form");
  const deleteArtistForm = document.getElementById("delete-artist-form");
  const artistOutput = document.getElementById("artist-output");

  // Create Artist
  createArtistForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createArtistForm);
    const response = await fetch("/artist/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    artistOutput.innerHTML = `<p>${result.message}</p><p>ArtistID: ${result.ArtistID}</p>`;
  });

  // Update Artist
  updateArtistForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateArtistForm);
    const artistId = formData.get("artistId");
    const response = await fetch(`/artist/${artistId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    artistOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Delete Artist
  deleteArtistForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteArtistForm);
    const artistId = formData.get("artistId");
    const response = await fetch(`/artist/${artistId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    artistOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // User Review Management (already present)
  const createReviewForm = document.getElementById("create-review-form");
  const updateReviewForm = document.getElementById("update-review-form");
  const deleteReviewForm = document.getElementById("delete-review-form");
  const reviewOutput = document.getElementById("review-output");

  // Create Review
  createReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(createReviewForm);
    const songId = formData.get("songId");
    const response = await fetch(`/review/${songId}`, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    reviewOutput.innerHTML = `<p>${result.message}</p><p>ReviewID: ${result.ReviewID}</p>`;
  });

  // Update Review
  updateReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateReviewForm);
    const reviewId = formData.get("reviewId");
    const response = await fetch(`/review/${reviewId}`, {
      method: "PUT",
      body: formData,
    });

    const result = await response.json();
    reviewOutput.innerHTML = `<p>${result.message}</p><p>ReviewID: ${result.ReviewID}</p>`;
  });

  // Delete Review
  deleteReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteReviewForm);
    const reviewId = formData.get("reviewId");
    const response = await fetch(`/review/${reviewId}`, {
      method: "DELETE",
    });

    const result = await response.json();
    reviewOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Create User Review Management
  const createUserReviewForm = document.getElementById(
    "create-user-review-form",
  );
  const createUserReviewOutput = document.getElementById("user-review-output");

  createUserReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent the default form submission behavior
    const formData = new FormData(createUserReviewForm);
    console.log(formData);

    const response = await fetch("/user_review/", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    createUserReviewOutput.innerHTML = `<p>${result.message}</p>`;
  });

  // Update User Review Management
  const updateUserReviewForm = document.getElementById(
    "update-user-review-form",
  );
  const updateUserReviewOutput = document.getElementById("user-review-output");

  updateUserReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(updateUserReviewForm);
    const userId = formData.get("userId");
    const reviewId = formData.get("reviewId");

    try {
      const response = await fetch(`/user_review/${userId}/${reviewId}`, {
        method: "PUT",
        body: formData,
      });

      const result = await response.json();
      updateUserReviewOutput.innerHTML = `<p>${result.message}</p>`;
    } catch (error) {
      updateUserReviewOutput.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });

  // Delete User Review Management
  const deleteUserReviewForm = document.getElementById(
    "delete-user-review-form",
  );
  const deleteUserReviewOutput = document.getElementById("user-review-output");

  deleteUserReviewForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(deleteUserReviewForm);
    const userId = formData.get("userId");
    const reviewId = formData.get("reviewId");

    try {
      const response = await fetch(`/user_review/${userId}/${reviewId}`, {
        method: "DELETE",
      });

      const result = await response.json();
      deleteUserReviewOutput.innerHTML = `<p>${result.message}</p>`;
    } catch (error) {
      deleteUserReviewOutput.innerHTML = `<p>Error: ${error.message}</p>`;
    }
  });
});
