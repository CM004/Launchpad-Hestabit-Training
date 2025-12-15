const mongoose = require("../mongodb/mongo");
const express = require("express");
const app = express();
app.get("/",(req,res)=>{
    res.json({
        message:"hello docker",
        status: "ok",
        db: mongoose.connection.readyState === 1 ? "connected" : "disconnected" 
    });
});

app.listen(9000,()=>console.log("server running at port 9000"));