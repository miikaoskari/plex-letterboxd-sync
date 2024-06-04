import { ProgressBar } from "../components/ProgressBar";
import { Button } from "../components/Button";
import { useEffect, useState, useRef } from "react";

export default function Root() {
  const [progress, setProgress] = useState(0);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("/ws");
    ws.current.onopen = () => {
      console.log("Connected to server");
    };

    ws.current.onmessage = (event) => {
      const message = JSON.parse(event.data);

      switch (message.type) {
        case "progress":
          console.log("status: ", message.status);
          setProgress(message.value);
          break;
        default:
          console.error("Unknown message type", message.type);
      }
    };

    ws.current.onclose = () => {
      console.log("Disconnected from server");
    };

    ws.current.onerror = (error) => {
      console.error(error);
    };

    return () => {
      ws.current.close();
    };
  }, []);

  const startSync = () => {
    if (ws.current) {
      console.log("Sending start_sync")
      ws.current.send("start_sync");
    }
  };

  return (
    <>
    <div className={"flex justify-center m-4"}>
      <h1 className={"text-4xl font-bold text-white mt-4 text-center"}>Plex-Letterboxd-Sync</h1>
    </div>
    <div className={"flex justify-center mt-12"}>
      <Button className={"mr-4"} onPress={startSync}>Start Sync</Button>
      <ProgressBar className={""} label={"Syncing..."} value={progress} />
    </div>
    </>
  );
}
