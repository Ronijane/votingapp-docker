import express from "express";
import cors from "cors";
import { createClient } from "redis";

const app = express();
app.use(cors());
app.use(express.json());

const redis = createClient({
  url: "redis://redis:6379"
});

redis.connect();

const candidates = ["Python", "JavaScript", "Go"];

app.get("/votes", async (req, res) => {
  const results = {};
  for (const c of candidates) {
    results[c] = parseInt(await redis.get(c)) || 0;
  }
  res.json(results);
});

app.post("/vote", async (req, res) => {
  const { candidate } = req.body;
  if (!candidates.includes(candidate)) {
    return res.status(400).json({ error: "Invalid candidate" });
  }

  await redis.incr(candidate);
  res.json({ message: "Vote recorded" });
});

app.listen(3000, () => {
  console.log("Backend running on port 3000");
});
