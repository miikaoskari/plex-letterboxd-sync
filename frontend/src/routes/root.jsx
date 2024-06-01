import {ProgressBar} from "../components/ProgressBar";
import {Button} from "../components/Button";

export default function Root() {
  return (
    <>
    <div className={"flex justify-center m-4"}>
      <h1 className={"text-4xl font-bold text-white mt-4 text-center"}>Plex-Letterboxd-Sync</h1>
    </div>
    <div className={"flex justify-center mt-12"}>
        <Button className={"mr-4"}>Start Sync</Button>
        <ProgressBar className={""} />
    </div>
    </>
  );
}
