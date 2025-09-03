import { useEffect, useMemo, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

const API = (import.meta.env.VITE_API_BASE as string) || "http://localhost:8000";

type Parcel = {
  id: number;
  parcel_id?: string;
  apn?: string;
  owner_name?: string;
  owner_id?: number;
  county?: string;
  state?: string;
  country?: string;
  acreage?: number;
  address?: string;
  status?: string;
  score?: number;
  valuation?: number;
  offer_min?: number;
  offer_max?: number;
  campaign_id?: number;
};

type Campaign = { id: number; name: string; channel?: string; description?: string; status?: string };

type AuctionSource = { id: number; name: string; url: string; county?: string; state?: string; country?: string };

function useCompanyInfo() {
  const [company, setCompany] = useState(() => {
    const raw = localStorage.getItem("company_info");
    return raw ? JSON.parse(raw) : { name: "", buyer_name: "", phone: "", email: "", address: "" };
  });
  useEffect(() => {
    localStorage.setItem("company_info", JSON.stringify(company));
  }, [company]);
  return { company, setCompany } as const;
}

export default function App() {
  const [tab, setTab] = useState("map");
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const mapRef = useRef<HTMLDivElement | null>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);
  const [filters, setFilters] = useState({ county: "", state: "", status: "" });
  const [parcels, setParcels] = useState<Parcel[]>([]);
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [sources, setSources] = useState<AuctionSource[]>([]);
  const { company, setCompany } = useCompanyInfo();

  useEffect(() => {
    if (mapRef.current && !mapInstance.current) {
      const map = new maplibregl.Map({
        container: mapRef.current,
        style: "https://demotiles.maplibre.org/style.json",
        center: [-98, 39],
        zoom: 3,
      });
      map.on("load", () => refreshGeoJSON(map));
      mapInstance.current = map;
    }
  }, []);

  async function refreshGeoJSON(map?: maplibregl.Map) {
    try {
      const qs = new URLSearchParams(Object.entries(filters).filter(([_, v]) => v));
      const res = await fetch(`${API}/parcels/geojson?${qs.toString()}`);
      const data = await res.json();
      const m = map || mapInstance.current!;
      const src = m.getSource("parcels") as maplibregl.GeoJSONSource | undefined;
      if (src) {
        src.setData(data as any);
      } else {
        m.addSource("parcels", { type: "geojson", data });
        m.addLayer({ id: "parcels-fill", type: "fill", source: "parcels", paint: { "fill-color": "#3b82f6", "fill-opacity": 0.2 } });
        m.addLayer({ id: "parcels-outline", type: "line", source: "parcels", paint: { "line-color": "#1d4ed8", "line-width": 1 } });
      }
    } catch {}
  }

  async function handleUpload(endpoint: "/parcels/ingest-csv" | "/parcels/ingest-xlsx" | "/parcels/ingest-shapefile") {
    if (!file) return;
    setUploading(true);
    setMessage("");
    try {
      const form = new FormData();
      form.append("file", file);
      const res = await fetch(`${API}${endpoint}`, { method: "POST", body: form });
      const json = await res.json();
      setMessage(`Ingested ${json.ingested} rows`);
      await refreshGeoJSON();
      await loadParcels();
    } catch (err) {
      setMessage("Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function loadParcels() {
    const qs = new URLSearchParams(Object.entries(filters).filter(([_, v]) => v));
    const res = await fetch(`${API}/parcels?${qs.toString()}`);
    const data = (await res.json()) as Parcel[];
    setParcels(data);
  }

  async function loadCampaigns() {
    const res = await fetch(`${API}/campaigns/`);
    const data = (await res.json()) as Campaign[];
    setCampaigns(data);
  }

  async function loadSources() {
    const res = await fetch(`${API}/auctions/sources`);
    setSources(await res.json());
  }

  useEffect(() => {
    loadParcels();
    loadCampaigns();
    loadSources();
  }, []);

  useEffect(() => {
    loadParcels();
    refreshGeoJSON();
  }, [filters]);

  async function updateParcel(p: Parcel, patch: Partial<Parcel>) {
    const res = await fetch(`${API}/parcels/${p.id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) });
    const updated = (await res.json()) as Parcel;
    setParcels((prev) => prev.map((x) => (x.id === updated.id ? updated : x)));
    await refreshGeoJSON();
  }

  function ContractGenerator() {
    const [country, setCountry] = useState("US");
    const [fields, setFields] = useState({ buyer_name: company.buyer_name || company.name || "", seller_name: "", parcel_id: "", apn: "", county: "", state: "", price: "", closing_date: "", closing_location: "" });

    const template = useMemo(() => {
      if (country === "US") {
        return (
`# Purchase Agreement\n\nBuyer: {{buyer_name}}\n\nSeller: {{seller_name}}\n\nParcel ID: {{parcel_id}} (APN: {{apn}})\n\nCounty/State: {{county}}, {{state}}\n\nPurchase Price: ${{price}} USD\n\nClosing: {{closing_date}} at {{closing_location}}\n\nThis agreement is governed by the laws of the state of {{state}}.`
        );
      }
      return (
`# Purchase Agreement (Nigeria)\n\nBuyer: {{buyer_name}}\n\nSeller: {{seller_name}}\n\nParcel ID: {{parcel_id}}\n\nLGA/State: {{county}}, {{state}}\n\nPurchase Price: ₦{{price}} NGN\n\nClosing: {{closing_date}} at {{closing_location}}\n\nThis agreement is governed by the laws of the Federal Republic of Nigeria.`
      );
    }, [country]);

    const merged = useMemo(() => {
      return template.replace(/{{(\w+)}}/g, (_, k) => (fields as any)[k] || "");
    }, [template, fields]);

    return (
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Details</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label>Country</Label>
                <Select value={country} onValueChange={setCountry}>
                  <SelectTrigger><SelectValue placeholder="Select country" /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="US">United States</SelectItem>
                    <SelectItem value="NG">Nigeria</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Buyer Name</Label>
                <Input value={fields.buyer_name} onChange={(e) => setFields({ ...fields, buyer_name: e.target.value })} />
              </div>
              <div>
                <Label>Seller Name</Label>
                <Input value={fields.seller_name} onChange={(e) => setFields({ ...fields, seller_name: e.target.value })} />
              </div>
              <div>
                <Label>Parcel ID</Label>
                <Input value={fields.parcel_id} onChange={(e) => setFields({ ...fields, parcel_id: e.target.value })} />
              </div>
              <div>
                <Label>APN</Label>
                <Input value={fields.apn} onChange={(e) => setFields({ ...fields, apn: e.target.value })} />
              </div>
              <div>
                <Label>County/LGA</Label>
                <Input value={fields.county} onChange={(e) => setFields({ ...fields, county: e.target.value })} />
              </div>
              <div>
                <Label>State</Label>
                <Input value={fields.state} onChange={(e) => setFields({ ...fields, state: e.target.value })} />
              </div>
              <div>
                <Label>Price</Label>
                <Input value={fields.price} onChange={(e) => setFields({ ...fields, price: e.target.value })} />
              </div>
              <div>
                <Label>Closing Date</Label>
                <Input value={fields.closing_date} onChange={(e) => setFields({ ...fields, closing_date: e.target.value })} />
              </div>
              <div>
                <Label>Closing Location</Label>
                <Input value={fields.closing_location} onChange={(e) => setFields({ ...fields, closing_location: e.target.value })} />
              </div>
            </div>
            <Button onClick={() => window.print()}>Print / Save as PDF</Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Preview</CardTitle></CardHeader>
          <CardContent>
            <pre className="whitespace-pre-wrap text-sm">{merged}</pre>
          </CardContent>
        </Card>
      </div>
    );
  }

  function Outreach() {
    const [to, setTo] = useState("");
    const [subject, setSubject] = useState("Regarding your parcel");
    const [body, setBody] = useState("Hello {{owner_name}},\n\nI'm interested in buying your land (Parcel: {{parcel_id}}). Let's talk.\n\nThanks,");
    const [selectedParcel, setSelectedParcel] = useState<string>("");
    const [selectedCampaign, setSelectedCampaign] = useState<string>("");
    const resolvedBody = useMemo(() => {
      const p = parcels.find(x => String(x.id) === selectedParcel);
      return body.replace("{{owner_name}}", p?.owner_name || "").replace("{{parcel_id}}", p?.parcel_id || String(p?.id || ""));
    }, [body, selectedParcel, parcels]);

    return (
      <Card>
        <CardHeader><CardTitle>Email Outreach</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div className="grid md:grid-cols-2 gap-3">
            <div>
              <Label>To</Label>
              <Input value={to} onChange={(e) => setTo(e.target.value)} placeholder="owner@example.com" />
            </div>
            <div>
              <Label>Parcel</Label>
              <Select value={selectedParcel} onValueChange={setSelectedParcel}>
                <SelectTrigger><SelectValue placeholder="Select parcel" /></SelectTrigger>
                <SelectContent>
                  {parcels.map(p => <SelectItem key={p.id} value={String(p.id)}>{p.parcel_id || p.id} · {p.owner_name || '-'}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Campaign</Label>
              <Select value={selectedCampaign} onValueChange={setSelectedCampaign}>
                <SelectTrigger><SelectValue placeholder="Select campaign" /></SelectTrigger>
                <SelectContent>
                  {campaigns.map(c => <SelectItem key={c.id} value={String(c.id)}>{c.name}</SelectItem>)}
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Subject</Label>
              <Input value={subject} onChange={(e) => setSubject(e.target.value)} />
            </div>
          </div>
          <div>
            <Label>Body</Label>
            <Textarea value={body} onChange={(e) => setBody(e.target.value)} rows={8} />
            <div className="mt-2 rounded border p-2 text-sm text-muted-foreground">
              <div className="font-medium">Preview</div>
              <pre className="whitespace-pre-wrap">{resolvedBody}</pre>
            </div>
          </div>
          <Button onClick={async () => {
            await fetch(`${API}/outreach/email`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ to, subject, body: resolvedBody, parcel_id: selectedParcel ? Number(selectedParcel) : undefined, campaign_id: selectedCampaign ? Number(selectedCampaign) : undefined }) });
          }}>Send Email</Button>
        </CardContent>
      </Card>
    );
  }

  function Auctions() {
    const [name, setName] = useState("");
    const [url, setUrl] = useState("");
    const [county, setCounty] = useState("");
    const [state, setState] = useState("");

    return (
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Add Source</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <Label>Name</Label>
            <Input value={name} onChange={(e) => setName(e.target.value)} />
            <Label>URL</Label>
            <Input value={url} onChange={(e) => setUrl(e.target.value)} />
            <div className="grid grid-cols-2 gap-2">
              <div>
                <Label>County</Label>
                <Input value={county} onChange={(e) => setCounty(e.target.value)} />
              </div>
              <div>
                <Label>State</Label>
                <Input value={state} onChange={(e) => setState(e.target.value)} />
              </div>
            </div>
            <Button onClick={async () => { await fetch(`${API}/auctions/sources?name=${encodeURIComponent(name)}&url=${encodeURIComponent(url)}&county=${encodeURIComponent(county)}&state=${encodeURIComponent(state)}`, { method: 'POST' }); await loadSources(); }}>Add</Button>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Sources</CardTitle></CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {sources.map(s => (
                <li key={s.id} className="flex items-center justify-between rounded border p-2">
                  <div>
                    <div className="font-medium">{s.name}</div>
                    <div className="text-xs text-muted-foreground">{s.url}</div>
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={async () => { await fetch(`${API}/auctions/run/${s.id}`, { method: 'POST' }); }}>Run</Button>
                    <Button variant="outline" size="sm" onClick={async () => { await fetch(`${API}/auctions/sources/${s.id}`, { method: 'DELETE' }); await loadSources(); }}>Delete</Button>
                  </div>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-7xl p-4">
        <Tabs value={tab} onValueChange={setTab}>
          <TabsList className="flex flex-wrap">
            <TabsTrigger value="map">Map</TabsTrigger>
            <TabsTrigger value="import">Import</TabsTrigger>
            <TabsTrigger value="crm">CRM</TabsTrigger>
            <TabsTrigger value="campaigns">Campaigns</TabsTrigger>
            <TabsTrigger value="outreach">Outreach</TabsTrigger>
            <TabsTrigger value="auctions">Auctions</TabsTrigger>
            <TabsTrigger value="contracts">Contracts</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>
          <TabsContent value="map" className="mt-4">
            <div className="grid gap-4 md:grid-cols-4">
              <Card className="md:col-span-1">
                <CardHeader><CardTitle>Filters</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                  <div>
                    <Label>County/LGA</Label>
                    <Input value={filters.county} onChange={(e) => setFilters({ ...filters, county: e.target.value })} />
                  </div>
                  <div>
                    <Label>State</Label>
                    <Input value={filters.state} onChange={(e) => setFilters({ ...filters, state: e.target.value })} />
                  </div>
                  <div>
                    <Label>Status</Label>
                    <Input value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })} />
                  </div>
                  <Button onClick={() => { loadParcels(); refreshGeoJSON(); }}>Apply</Button>
                </CardContent>
              </Card>
              <Card className="md:col-span-3">
                <CardHeader><CardTitle>Parcels Map</CardTitle></CardHeader>
                <CardContent>
                  <div ref={mapRef} className="h-[600px] w-full rounded-md border" />
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="import" className="mt-4">
            <Card>
              <CardHeader><CardTitle>Bulk Import</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                <Input type="file" accept=".csv,.txt,.xlsx,.xls,.zip" onChange={(e) => setFile(e.target.files?.[0] || null)} />
                <div className="flex flex-wrap gap-2">
                  <Button disabled={!file || uploading} onClick={() => handleUpload("/parcels/ingest-csv")}>{uploading ? "Uploading..." : "Upload CSV"}</Button>
                  <Button variant="secondary" disabled={!file || uploading} onClick={() => handleUpload("/parcels/ingest-xlsx")}>{uploading ? "Uploading..." : "Upload XLSX"}</Button>
                  <Button variant="outline" disabled={!file || uploading} onClick={() => handleUpload("/parcels/ingest-shapefile")}>{uploading ? "Uploading..." : "Upload Shapefile ZIP"}</Button>
                </div>
                {message && <p className="text-sm text-muted-foreground">{message}</p>}
                <p className="text-xs text-muted-foreground">Columns supported: parcel_id, apn, owner_name, county, state, country, acreage, address, geom_wkt, status. Shapefiles: ZIP with .shp/.dbf/.shx</p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="crm" className="mt-4">
            <Card>
              <CardHeader><CardTitle>Parcels</CardTitle></CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left">
                        <th className="p-2">ID</th>
                        <th className="p-2">Owner</th>
                        <th className="p-2">County</th>
                        <th className="p-2">State</th>
                        <th className="p-2">Acreage</th>
                        <th className="p-2">Status</th>
                        <th className="p-2">Campaign</th>
                        <th className="p-2">Score</th>
                        <th className="p-2"></th>
                      </tr>
                    </thead>
                    <tbody>
                      {parcels.map((p) => (
                        <tr key={p.id} className="border-t">
                          <td className="p-2">{p.id}</td>
                          <td className="p-2">{p.owner_name || "-"}</td>
                          <td className="p-2">{p.county || "-"}</td>
                          <td className="p-2">{p.state || "-"}</td>
                          <td className="p-2">{p.acreage ?? "-"}</td>
                          <td className="p-2">
                            <Select value={p.status || "lead"} onValueChange={(v) => updateParcel(p, { status: v })}>
                              <SelectTrigger className="w-[150px]"><SelectValue /></SelectTrigger>
                              <SelectContent>
                                {['lead','contacted','negotiating','contract_sent','closed','dead'].map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}
                              </SelectContent>
                            </Select>
                          </td>
                          <td className="p-2">
                            <Select value={String(p.campaign_id || "none")} onValueChange={(v) => updateParcel(p, { campaign_id: v === 'none' ? undefined : Number(v) })}>
                              <SelectTrigger className="w-[160px]"><SelectValue /></SelectTrigger>
                              <SelectContent>
                                <SelectItem value="none">None</SelectItem>
                                {campaigns.map((c) => (
                                  <SelectItem key={c.id} value={String(c.id)}>{c.name}</SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                          </td>
                          <td className="p-2">{p.score ?? "-"}</td>
                          <td className="p-2 text-right">
                            <Button size="sm" variant="outline" onClick={() => window.open(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(p.address || '')}`, "_blank")}>Maps</Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="mt-3 flex gap-2">
                  <Button onClick={loadParcels}>Refresh</Button>
                  <Button variant="secondary" onClick={async () => { await fetch(`${API}/ml/score`, { method: 'POST' }); await loadParcels(); }}>Run Scoring</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="campaigns" className="mt-4">
            <div className="grid gap-4 md:grid-cols-2">
              <Card>
                <CardHeader><CardTitle>Create Campaign</CardTitle></CardHeader>
                <CardContent className="space-y-3">
                  <Label>Name</Label>
                  <Input id="camp_name" placeholder="e.g. Q4 Cold Call" />
                  <Label>Channel</Label>
                  <Input id="camp_channel" placeholder="dialer / sms / email / whatsapp" />
                  <Label>Description</Label>
                  <Textarea id="camp_desc" placeholder="What is this campaign about?" />
                  <Button onClick={async () => {
                    const name = (document.getElementById('camp_name') as HTMLInputElement).value;
                    const channel = (document.getElementById('camp_channel') as HTMLInputElement).value;
                    const description = (document.getElementById('camp_desc') as HTMLTextAreaElement).value;
                    await fetch(`${API}/campaigns/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, channel, description }) });
                    await loadCampaigns();
                  }}>Create</Button>
                </CardContent>
              </Card>
              <Card>
                <CardHeader><CardTitle>Campaigns</CardTitle></CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {campaigns.map((c) => (
                      <li key={c.id} className="flex items-center justify-between rounded border p-2">
                        <div>
                          <div className="font-medium">{c.name}</div>
                          <div className="text-xs text-muted-foreground">{c.channel || '-'} · {c.status || 'active'}</div>
                        </div>
                        <Button variant="outline" size="sm" onClick={async () => { await fetch(`${API}/campaigns/${c.id}`, { method: 'DELETE' }); await loadCampaigns(); }}>Delete</Button>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="outreach" className="mt-4">
            <Outreach />
          </TabsContent>

          <TabsContent value="auctions" className="mt-4">
            <Auctions />
          </TabsContent>

          <TabsContent value="contracts" className="mt-4">
            <ContractGenerator />
          </TabsContent>

          <TabsContent value="settings" className="mt-4">
            <Card>
              <CardHeader><CardTitle>Company Info</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <Label>Company Name</Label>
                    <Input value={company.name} onChange={(e) => setCompany({ ...company, name: e.target.value })} />
                  </div>
                  <div>
                    <Label>Buyer Name</Label>
                    <Input value={company.buyer_name} onChange={(e) => setCompany({ ...company, buyer_name: e.target.value })} />
                  </div>
                  <div>
                    <Label>Phone</Label>
                    <Input value={company.phone} onChange={(e) => setCompany({ ...company, phone: e.target.value })} />
                  </div>
                  <div>
                    <Label>Email</Label>
                    <Input value={company.email} onChange={(e) => setCompany({ ...company, email: e.target.value })} />
                  </div>
                  <div className="col-span-2">
                    <Label>Address</Label>
                    <Input value={company.address} onChange={(e) => setCompany({ ...company, address: e.target.value })} />
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
