import { ProgressBar } from "../components/ProgressBar";
import { Button } from "../components/Button";
import { useState } from "react";

export default function Root() {
  const [progress, setProgress] = useState(0);

  async function startSync() {
    console.log("Starting sync");
    setProgress(1);
    
    const url = "/api/sync"

    const response = await fetch(url, {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json"
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",

    });
    return response.json();
  }

  return (
    <>
    <div className={"flex justify-center m-4"}>
      <h1 className={"text-4xl font-bold text-white mt-4 text-center"}>Plex-Letterboxd-Sync</h1>
    </div>
    <div className={"flex justify-center mt-12"}>
      <Button className={"mr-4"} onPress={() => startSync}>Start Sync</Button>
      <ProgressBar className={""} label={"Syncing..."} value={progress} />
    </div>
    </>
  );
}
