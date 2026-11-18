#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <sstream>

using namespace std;

struct CasoPrueba {
    string titulo;
    int n;
    vector<string> etiquetas;
    vector<pair<int, int>> aristas;
    vector<vector<int>> adj;
    vector<string> eventos_json;
    bool es_dag = true;
    vector<int> pila_final;
    vector<int> orden_topologico;
};

string vectorToJsonArray(const vector<int>& v) {
    stringstream ss;
    ss << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        ss << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    ss << "]";
    return ss.str();
}

bool dfs(
    int u,
    CasoPrueba& caso,
    vector<int>& estado,
    vector<int>& tin,
    vector<int>& tout,
    vector<int>& orden,
    int& reloj
) {
    estado[u] = 1; // en proceso
    tin[u] = ++reloj;

    {
        stringstream ev;
        ev << "      {\"tipo\": \"iniciar_nodo\", \"u\": " << u
           << ", \"estado\": 1, \"tin\": " << tin[u] << ", \"tout\": -1"
           << ", \"mensaje\": \"Descubriendo nodo " << caso.etiquetas[u]
           << " (estado = 1, tin = " << tin[u] << ")\"}";
        caso.eventos_json.push_back(ev.str());
    }

    for (int v : caso.adj[u]) {
        if (estado[v] == 1) {
            stringstream ev;
            ev << "      {\"tipo\": \"ciclo_detectado\", \"u\": " << u
               << ", \"v\": " << v << ", \"estado_v\": 1"
               << ", \"mensaje\": \"¡Ciclo detectado! Arista (" << u << " -> " << v
               << ") apunta a un nodo en proceso (estado == 1)\"}";
            caso.eventos_json.push_back(ev.str());
            return true; // se encontró un ciclo dirigido
        }

        if (estado[v] == 0) {
            {
                stringstream ev;
                ev << "      {\"tipo\": \"explorar_arista\", \"u\": " << u
                   << ", \"v\": " << v << ", \"estado_v\": 0"
                   << ", \"mensaje\": \"Explorando arista (" << u << " -> " << v
                   << "): destino no visitado (estado = 0)\"}";
                caso.eventos_json.push_back(ev.str());
            }
            if (dfs(v, caso, estado, tin, tout, orden, reloj)) {
                return true;
            }
        } else if (estado[v] == 2) {
            stringstream ev;
            ev << "      {\"tipo\": \"arista_visitada\", \"u\": " << u
               << ", \"v\": " << v << ", \"estado_v\": 2"
               << ", \"mensaje\": \"Arista (" << u << " -> " << v
               << "): destino ya terminado (estado = 2, tout = " << tout[v] << ")\"}";
            caso.eventos_json.push_back(ev.str());
        }
    }

    estado[u] = 2; // terminado
    tout[u] = ++reloj;
    orden.push_back(u);

    {
        stringstream ev;
        ev << "      {\"tipo\": \"finalizar_nodo\", \"u\": " << u
           << ", \"estado\": 2, \"tin\": " << tin[u] << ", \"tout\": " << tout[u]
           << ", \"pila\": " << vectorToJsonArray(orden)
           << ", \"mensaje\": \"Nodo " << caso.etiquetas[u]
           << " terminado (tout = " << tout[u] << "). Apilado en orden.\"}";
        caso.eventos_json.push_back(ev.str());
    }

    return false;
}

void ejecutarTopologicalSort(CasoPrueba& caso) {
    int n = caso.n;
    vector<int> estado(n, 0);
    vector<int> tin(n, -1);
    vector<int> tout(n, -1);
    vector<int> orden;
    orden.reserve(n);
    int reloj = 0;

    for (int i = 0; i < n; ++i) {
        if (estado[i] == 0) {
            if (dfs(i, caso, estado, tin, tout, orden, reloj)) {
                caso.es_dag = false;
                stringstream ev;
                ev << "      {\"tipo\": \"resultado_final\", \"es_dag\": false"
                   << ", \"pila_final\": [], \"orden_topologico\": []"
                   << ", \"mensaje\": \"Ejecución abortada: el grafo contiene un ciclo dirigido.\"}";
                caso.eventos_json.push_back(ev.str());
                return;
            }
        }
    }

    caso.es_dag = true;
    caso.pila_final = orden;
    reverse(orden.begin(), orden.end());
    caso.orden_topologico = orden;

    stringstream ev;
    ev << "      {\"tipo\": \"resultado_final\", \"es_dag\": true"
       << ", \"pila_final\": " << vectorToJsonArray(caso.pila_final)
       << ", \"orden_topologico\": " << vectorToJsonArray(caso.orden_topologico)
       << ", \"mensaje\": \"Pila invertida: Orden Topológico válido obtenido.\"}";
    caso.eventos_json.push_back(ev.str());
}

void escribirCasoJson(ofstream& out, const string& clave, const CasoPrueba& caso, bool ultimo) {
    out << "  \"" << clave << "\": {\n";
    out << "    \"titulo\": \"" << caso.titulo << "\",\n";
    out << "    \"n\": " << caso.n << ",\n";

    out << "    \"etiquetas\": [";
    for (size_t i = 0; i < caso.etiquetas.size(); ++i) {
        out << "\"" << caso.etiquetas[i] << "\"" << (i + 1 < caso.etiquetas.size() ? ", " : "");
    }
    out << "],\n";

    out << "    \"aristas\": [";
    for (size_t i = 0; i < caso.aristas.size(); ++i) {
        out << "[" << caso.aristas[i].first << ", " << caso.aristas[i].second << "]"
            << (i + 1 < caso.aristas.size() ? ", " : "");
    }
    out << "],\n";

    out << "    \"eventos\": [\n";
    for (size_t i = 0; i < caso.eventos_json.size(); ++i) {
        out << caso.eventos_json[i] << (i + 1 < caso.eventos_json.size() ? ",\n" : "\n");
    }
    out << "    ]\n";
    out << "  }" << (ultimo ? "\n" : ",\n");
}

int main() {
    // CASO 1: DAG limpio de 6 nodos (Prerrequisitos de cursos universitarios)
    CasoPrueba casoDag;
    casoDag.titulo = "DAG de Prerrequisitos de Cursos (6 Nodos)";
    casoDag.n = 6;
    casoDag.etiquetas = {
        "0: PROG1",
        "1: BD1",
        "2: PROG2",
        "3: AED",
        "4: PROG3",
        "5: BD2"
    };
    casoDag.aristas = {
        {0, 2}, // PROG1 -> PROG2
        {2, 4}, // PROG2 -> PROG3
        {4, 3}, // PROG3 -> AED
        {2, 1}, // PROG2 -> BD1
        {3, 5}, // AED -> BD2
        {1, 5}  // BD1 -> BD2
    };
    casoDag.adj.resize(casoDag.n);
    for (auto [u, v] : casoDag.aristas) {
        casoDag.adj[u].push_back(v);
    }

    ejecutarTopologicalSort(casoDag);

    cout << "=== CASO 1: " << casoDag.titulo << " ===\n";
    cout << "Orden Topologico (Tarjan): ";
    for (int u : casoDag.orden_topologico) {
        cout << "[" << casoDag.etiquetas[u] << "] ";
    }
    cout << "\n\n";

    // CASO 2: Caso borde con ciclo dirigido (4 módulos con dependencia circular)
    CasoPrueba casoCiclo;
    casoCiclo.titulo = "Caso Borde: Detección de Ciclo Dirigido";
    casoCiclo.n = 4;
    casoCiclo.etiquetas = {
        "0: Auth",
        "1: Core",
        "2: API",
        "3: DB"
    };
    casoCiclo.aristas = {
        {0, 1},
        {1, 2},
        {2, 3},
        {3, 1}  // Arista de retroceso hacia nodo 1 (estado == 1)
    };
    casoCiclo.adj.resize(casoCiclo.n);
    for (auto [u, v] : casoCiclo.aristas) {
        casoCiclo.adj[u].push_back(v);
    }

    ejecutarTopologicalSort(casoCiclo);

    cout << "=== CASO 2: " << casoCiclo.titulo << " ===\n";
    cout << "Resultado: " << (casoCiclo.es_dag ? "DAG Valido" : "Ciclo detectado (Sin orden topologico)") << "\n\n";

    // Exportar traza completa a traza.json
    ofstream out("traza.json");
    if (!out.is_open()) {
        cerr << "Error al crear traza.json\n";
        return 1;
    }

    out << "{\n";
    escribirCasoJson(out, "caso_dag", casoDag, false);
    escribirCasoJson(out, "caso_ciclo", casoCiclo, true);
    out << "}\n";
    out.close();

    cout << "Archivo 'traza.json' exportado correctamente.\n";
    return 0;
}

