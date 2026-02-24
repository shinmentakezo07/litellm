import React, { useEffect, useMemo, useRef, useState } from "react";
import { Button, Card, Text, TextInput, Title } from "@tremor/react";

import {
  createOrUpdateKiroModel,
  getGeneralSettingsCall,
  updateKiroSettingField,
  updateKiroSettings,
} from "./networking";
import NotificationsManager from "./molecules/notifications_manager";

interface KiroSettingsProps {
  accessToken: string | null;
}

interface GeneralSettingsItem {
  field_name: string;
  field_value: any;
}

const DEFAULT_KIRO_MODEL_ID = "kiro_gateway/claude-sonnet-4-5";
const DEFAULT_KIRO_API_BASE = "http://localhost:8000/v1";
const DEFAULT_KIRO_MODEL_NAME = "kiro-gateway-default";

const KiroSettings: React.FC<KiroSettingsProps> = ({ accessToken }) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [saving, setSaving] = useState<boolean>(false);
  const [modelId, setModelId] = useState<string>(DEFAULT_KIRO_MODEL_ID);
  const [refreshToken, setRefreshToken] = useState<string>("");
  const [apiBase, setApiBase] = useState<string>(DEFAULT_KIRO_API_BASE);
  const [modelDbId, setModelDbId] = useState<string>("");

  const initializedRef = useRef<boolean>(false);

  const hasValues = useMemo(
    () => modelId.length > 0 || refreshToken.length > 0 || apiBase.length > 0 || modelDbId.length > 0,
    [modelId, refreshToken, apiBase, modelDbId],
  );

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
        const kiroApiBase = settings.find((item) => item.field_name === "kiro_api_base")?.field_value;
        const kiroModelDbId = settings.find((item) => item.field_name === "kiro_model_db_id")?.field_value;

        setModelId(typeof kiroModel === "string" && kiroModel.length > 0 ? kiroModel : DEFAULT_KIRO_MODEL_ID);
        setRefreshToken(typeof kiroToken === "string" ? kiroToken : "");
        setApiBase(typeof kiroApiBase === "string" && kiroApiBase.length > 0 ? kiroApiBase : DEFAULT_KIRO_API_BASE);
        setModelDbId(typeof kiroModelDbId === "string" ? kiroModelDbId : "");
      } catch (error) {
        console.error("Failed to load Kiro settings:", error);
      } finally {
        initializedRef.current = true;
        setLoading(false);
      }
    };

    loadSettings();
  }, [accessToken]);

  useEffect(() => {
    if (!accessToken || !initializedRef.current || loading) {
      return;
    }

    const saveModelId = async () => {
      setSaving(true);
      try {
        await updateKiroSettingField(accessToken, "kiro_model_id", modelId && modelId.trim().length > 0 ? modelId : null);
      } catch (error) {
        NotificationsManager.fromBackend(error);
      } finally {
        setSaving(false);
      }
    };

    saveModelId();
  }, [accessToken, modelId, loading]);

  useEffect(() => {
    if (!accessToken || !initializedRef.current || loading) {
      return;
    }

    const saveApiBase = async () => {
      setSaving(true);
      try {
        await updateKiroSettingField(accessToken, "kiro_api_base", apiBase && apiBase.trim().length > 0 ? apiBase : null);
      } catch (error) {
        NotificationsManager.fromBackend(error);
      } finally {
        setSaving(false);
      }
    };

    saveApiBase();
  }, [accessToken, apiBase, loading]);

  useEffect(() => {
    if (!accessToken || !initializedRef.current || loading) {
      return;
    }

    const saveRefreshTokenAndSyncModel = async () => {
      setSaving(true);
      try {
        const trimmedRefreshToken = refreshToken.trim();

        await updateKiroSettingField(
          accessToken,
          "kiro_refresh_token",
          trimmedRefreshToken.length > 0 ? trimmedRefreshToken : null,
        );

        if (trimmedRefreshToken.length > 0) {
          const modelResponse = await createOrUpdateKiroModel(accessToken, {
            modelName: DEFAULT_KIRO_MODEL_NAME,
            modelId: modelId.trim().length > 0 ? modelId : DEFAULT_KIRO_MODEL_ID,
            apiBase: apiBase.trim().length > 0 ? apiBase : DEFAULT_KIRO_API_BASE,
            modelDbId: modelDbId.trim().length > 0 ? modelDbId : null,
          });

          if (modelResponse.model_id && modelResponse.model_id !== modelDbId) {
            setModelDbId(modelResponse.model_id);
            await updateKiroSettingField(accessToken, "kiro_model_db_id", modelResponse.model_id);
          }
        }
      } catch (error) {
        NotificationsManager.fromBackend(error);
      } finally {
        setSaving(false);
      }
    };

    saveRefreshTokenAndSyncModel();
  }, [accessToken, refreshToken, modelId, apiBase, modelDbId, loading]);

  const onReset = async () => {
    if (!accessToken) {
      return;
    }

    setSaving(true);
    try {
      await updateKiroSettings(
        accessToken,
        {
          modelId: DEFAULT_KIRO_MODEL_ID,
          refreshToken: null,
          apiBase: DEFAULT_KIRO_API_BASE,
          modelDbId: null,
        },
        {
          silent: true,
        },
      );
      setModelId(DEFAULT_KIRO_MODEL_ID);
      setRefreshToken("");
      setApiBase(DEFAULT_KIRO_API_BASE);
      setModelDbId("");
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
        <Text className="text-gray-600">
          Configure Kiro gateway auto-save settings. LLM credentials and mapped model are synced to All Models automatically.
        </Text>
      </div>

      <Card className="shadow-sm p-6">
        {loading ? (
          <Text>Loading Kiro settings…</Text>
        ) : (
          <div className="space-y-6">
            <div>
              <Text className="text-sm font-medium text-gray-700 mb-2 block">Kiro Model ID</Text>
              <TextInput
                placeholder="kiro_gateway/claude-sonnet-4-5"
                value={modelId}
                onValueChange={setModelId}
                className="w-full"
                disabled={saving}
              />
              <Text className="text-xs text-gray-500 mt-1">Real model id used by kiro-gateway mapping.</Text>
            </div>

            <div>
              <Text className="text-sm font-medium text-gray-700 mb-2 block">Kiro API Base</Text>
              <TextInput
                placeholder={DEFAULT_KIRO_API_BASE}
                value={apiBase}
                onValueChange={setApiBase}
                className="w-full"
                disabled={saving}
              />
              <Text className="text-xs text-gray-500 mt-1">Gateway base url for kiro provider model mapping.</Text>
            </div>

            <div>
              <Text className="text-sm font-medium text-gray-700 mb-2 block">Kiro Refresh Token</Text>
              <TextInput
                placeholder="Enter Kiro refresh token"
                value={refreshToken}
                onValueChange={setRefreshToken}
                type="password"
                className="w-full"
                disabled={saving}
              />
              <Text className="text-xs text-gray-500 mt-1">
                Auto-saved to general settings. When set, mapped model is auto-created/updated in All Models.
              </Text>
            </div>

            {modelDbId ? (
              <div className="rounded-md border border-emerald-200 bg-emerald-50 p-3">
                <Text className="text-xs text-emerald-700">Mapped model synced in All Models (model_id: {modelDbId})</Text>
              </div>
            ) : null}

            <div className="flex gap-3 pt-4">
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
