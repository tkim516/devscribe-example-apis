const express = require("express");
const app = express();
app.use(express.json());

app.get("/users", (req, res) => {
    // Return list of users
    res.json([{ id: 1, name: "Alice" }]);
});

app.post("/users", (req, res) => {
    // Create a new user
    const name = req.body.name || "New User";
    res.json({ id: 2, name });
});

app.listen(3000, () => console.log("Running on port 3000"));