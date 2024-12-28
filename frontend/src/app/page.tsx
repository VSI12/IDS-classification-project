import Image from "next/image";
import UploadDataset from "../components/upload-dataset";
import ModelSelectionForm from "@/components/models";

export default function Home() {
  return (
    <div>
      <UploadDataset />
      <ModelSelectionForm/>
    </div>
  );
}
