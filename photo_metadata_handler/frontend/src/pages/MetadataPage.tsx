import MetadataEditor from "../components/MetadataEditor";

const MetadataPage = () => {
  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h2 className="text-2xl font-semibold mb-6">Image Metadata Editor</h2>
      <MetadataEditor />
    </div>
  );
};

export default MetadataPage;
