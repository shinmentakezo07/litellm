import React, { useEffect, useMemo, useState } from "react";
import { Button, Card, Text, TextInput, Title } from "@tremor/react";

import { getGeneralSettingsCall, updateKiroSettings } from "./networking";
import NotificationsManager from "./molecules/notifications_manager";

interface KiroSettingsProps {
  accessToken: string | null;
}

interface GeneralSettingsItem {
  field_name: string;
  field_value: any;
}

const KiroSettings: React.FC<KiroSettingsProps> = ({ accessToken }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [modelId, setModelId] = useState<string>("");
  const [refreshToken, setRefreshToken] = useState<string>("");

  const hasValues = useMemo(() => modelId.length > 0 || refreshToken.length > 0, [modelId, refreshToken]);

  useEffect(() => {
    if (!accessToken) {
      return;
    }

    const loadSettings = async () => {
      setLoading(true);
      try {
        const settings: GeneralSettingsItem[] = await getGeneralSettingsCall(accessToken);
        const kiroModel = settings.find((item) => item.field_name === "kiro_model_id")?.field_value;
        const kiroToken = settings.find((item) => item.field_name === "kiro_refresh_token")?.field_value;

        setModelId(typeof kiroModel === "string" ? kiroModel : "");
        setRefreshToken(typeof kiroToken === "string" ? kiroToken : "");
      } catch (error) {
        console.error("Failed to load Kiro settings:", error);
      } finally {
        setLoading(false);
      }
    };

    loadSettings();
  }, [accessToken]);

  const onSave = async () => {
    if (!accessToken) {
      return;
    }

    setSaving(true);
    try {
      await updateKiroSettings(accessToken, {
        modelId,
        refreshToken,
      });
    } catch (error) {
      NotificationsManager.fromBackend(error);
    } finally {
      setSaving(false);
    }
  };

  const onReset = async () => {
    if (!accessToken) {
      return;
    }

    setSaving(true);
    try {
      await updateKiroSettings(accessToken, {
        modelId: null,
        refreshToken: null,
      });
      setModelId("");
      setRefreshToken("");
      NotificationsManager.success("Kiro settings reset");
    } catch (error) {
      NotificationsManager.fromBackend(error);
    } finally {
      setSaving(false);
    }
  };

  if (!accessToken) {
    return null;
  }

  return (
    <div className="w-full mx-auto max-w-4xl px-6 py-8">
      <div className="mb-8">
        <Title className="text-2xl font-bold mb-2">Kiro Settings</Title>
        <Text className="text-gray-600">Configure the default Kiro model id and refresh token used by your dashboard setup.</Text>
      </div>

      <Card className="shadow-sm p-6">
        {loading ? (
          <Text>Loading Kiro settings…</Text>
        ) : (
          <div className="space-y-6">
            <div>
              <Text className="text-sm font-medium text-gray-700 mb-2 block">Kiro Model ID</Text>
              <TextInput
                placeholder="us.anthropic.claude-sonnet-4-20250514-v1:0"
                value={modelId}
                onValueChange={setModelId}
                className="w-full"
              />
              <Text className="text-xs text-gray-500 mt-1">Model id to use for Kiro calls in your environment.</Text>
            </div>

            <div>
              <Text className="text-sm font-medium text-gray-700 mb-2 block">Kiro Refresh Token</Text>
              <TextInput
                placeholder="Enter Kiro refresh token"
                value={refreshToken}
                onValueChange={setRefreshToken}
                type="password"
                className="w-full"
              />
              <Text className="text-xs text-gray-500 mt-1">Stored in proxy general settings and editable by admin users only.</Text>
            </div>

            <div className="flex gap-3 pt-4">
              <Button onClick={onSave} loading={saving} disabled={saving || (!modelId && !refreshToken)} color="indigo">
                Save Kiro Settings
              </Button>
              <Button onClick={onReset} loading={saving} disabled={saving || !hasValues} variant="secondary" color="gray">
                Reset
              </Button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default KiroSettings;
