export function renderPostImageCard(post) {
  const wrap = document.createElement("div");
  wrap.className = "postImageCard";

  const img = document.createElement("img");
  img.className = "postImageCard__img";
  img.src = post.image_url;
  img.alt = "";
  img.loading = "lazy";

  wrap.appendChild(img);
  return wrap;
}