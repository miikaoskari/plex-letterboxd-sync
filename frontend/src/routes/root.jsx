import { ProgressBar } from "../components/ProgressBar";
import { Button } from "../components/Button";
import { useEffect, useState, useRef } from "react";
import { ToastContainer, toast } from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

export default function Root() {
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("Idle");
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
          setStatus(message.status);
          if (message.value == 100) {
            setTimeout(() => {
              setProgress(0);
              setStatus("Idle");
            }, 10000);
          }
          break;
        default:
          console.error("Unknown message type", message.type);
      }
    };

    ws.current.onclose = () => {
      toast("Disconnected from server", { 
        position: "bottom-center",
        autoClose: 1000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        theme: "dark",
      });
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
      <ProgressBar className={""} label={status} value={progress} />
    </div>
    <div className={"flex justify-center mt-12"}>
      <ToastContainer />
    </div>
    </>
  );
}
