const API_BASE = "http://127.0.0.1:8000";

export async function uploadFileToBackend(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("File upload failed");
  }

  return await res.json();
}

export async function askQuestion(question, fileIds = []) {
  const res = await fetch("http://127.0.0.1:8000/query", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      file_ids: fileIds,
    }),
  });

  if (!res.ok) throw new Error("Query failed");
  return res.json();
}
