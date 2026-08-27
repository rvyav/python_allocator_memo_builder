import { useEffect, useState } from "react";
import httpRequest from "./api/HttpRequest";

interface HelloResponse {
  message: string;
}

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const getHelloWorld = async () => {
      try {
        const data = await httpRequest.get<HelloResponse>("/api/health/");

        setMessage(data.message);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    getHelloWorld();
  }, []);

  return (
    <div>
      <h1>{message}</h1>
    </div>
  );
}

export default App;