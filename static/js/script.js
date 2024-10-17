document.addEventListener("DOMContentLoaded", function () {
  const entities = [
    { name: "entry", idField: "entryId" },
    { name: "report", idField: "reportId" },
    { name: "user", idField: "userId" },
    { name: "song", idField: "songId" },
    { name: "platform", idField: "platformId" },
    { name: "album", idField: "albumId" },
    { name: "artist", idField: "artistId" },
    { name: "review", idField: "reviewId" },
    {
      name: "user-review",
      idField: ["userId", "reviewId"],
      basePath: "user_review",
    },
    {
      name: "artist-album",
      idField: ["artistId", "albumId"],
      basePath: "artist_album",
    },
  ];

  const handleFormSubmission = (
    form,
    output,
    entity,
    method,
    urlSuffix = "",
  ) => {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      const formData = new FormData(form);
      const url = constructUrl(entity, method, formData, urlSuffix);

      try {
        const response = await fetch(url, {
          method,
          body: method === "GET" || method === "DELETE" ? null : formData,
        });
        const result = await response.json();
        output.innerHTML = `<p>${result.message}</p>${
          result[entity.name + "ID"]
            ? `<p>${entity.name}ID: ${result[entity.name + "ID"]}</p>`
            : ""
        }`;
      } catch (error) {
        output.innerHTML = `<p>Error: ${error.message}</p>`;
      }
    });
  };

  const constructUrl = (entity, method, formData, urlSuffix) => {
    const basePath = entity.basePath || entity.name;
    const idFields = Array.isArray(entity.idField)
      ? entity.idField
      : [entity.idField];
    const ids = idFields
      .map((id) => formData.get(id))
      .filter(Boolean)
      .join("/");
    const url = `/${basePath}/${ids}${urlSuffix}`;
    return method === "POST" ? `/${basePath}/` : url;
  };

  entities.forEach((entity) => {
    const forms = ["create", "update", "delete"].map((action) =>
      document.getElementById(`${action}-${entity.name}-form`),
    );
    const output = document.getElementById(
      `${entity.name.replace("-", "_")}-output`,
    );

    if (forms[0]) handleFormSubmission(forms[0], output, entity, "POST");
    if (forms[1]) handleFormSubmission(forms[1], output, entity, "PUT");
    if (forms[2]) handleFormSubmission(forms[2], output, entity, "DELETE");
  });
});
