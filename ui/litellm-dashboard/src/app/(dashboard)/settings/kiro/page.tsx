"use client";

import useAuthorized from "@/app/(dashboard)/hooks/useAuthorized";
import KiroSettings from "@/components/kiro_settings";

const KiroSettingsPage = () => {
  const { accessToken } = useAuthorized();

  return <KiroSettings accessToken={accessToken} />;
};

export default KiroSettingsPage;
