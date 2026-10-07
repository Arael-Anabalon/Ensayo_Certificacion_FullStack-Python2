-- Inserción de datos para esquema_tasktrack
-- Ejecutar SIEMPRE despues de la creación del primer usuario (para que los datos se creen a su nombre)

-- Usar la DB
USE esquema_tasktrack;

-- Inserción de datos para tabla "categorias"
INSERT INTO categorias (nombre, descripcion, created_by) VALUES
    ("Estudios", "Gestión de asignaturas, entregas académicas y preparación de exámenes", "system"),
    ("Trabajo", "Seguimiento de proyectos laborales, reuniones con clientes y entregables", "system"),
    ("Salud", "Control de citas médicas, rutinas de ejercicio y bienestar general", "system"),
    ("Personal", "Metas individuales, organización del hogar y actividades de ocio", "system");

-- Inserción de datos para tabla "prioridades"
INSERT INTO prioridades (nombre, descripcion, created_by) VALUES
    ("Alta", "Requiere atención inmediata y prioritaria antes de finalizar la jornada", "system"),
    ("Media", "Importante pero con margen de tiempo manejable para su ejecución", "system"),
    ("Baja", "Actividad secundaria que puede postergarse sin impactar los objetivos generales", "system");

-- Inserción de datos para tabla "estados"
INSERT INTO estados (nombre, descripcion, created_by) VALUES
    ("Pendiente", "Planificada pero aún no se ha iniciado ninguna acción sobre ella", "system"),
    ("En progreso", "Se encuentra actualmente en ejecución activa por parte del usuario", "system"),
    ("Completada", "Finalizada con éxito cumpliendo todos los requisitos establecidos", "system");

-- Inserción de datos para tabla "tareas"
INSERT INTO tareas (titulo, categoria, prioridad, estado, fecha_limite, descripcion, usuario, created_by)
VALUES 
    (
        "Estudiar Flask",
        1,
        1,
        1,
        '2025-12-10',
        "Revisar la documentación oficial de Flask sobre ruteo dinámico y manejo de sesiones antes de la evaluación.",
        1,
        1
    ),
    (
        "Proyecto final",
        1,
        2,
        2,
        '2025-12-15',
        "Finalizar la integración de las consultas JOIN en los métodos de lectura del repositorio para la entrega.",
        1,
        1
    ),
    (
        "Reporte mensual",
        2,
        3,
        1,
        '2025-12-20',
        "Consolidar las métricas de rendimiento del equipo y enviar el documento al director del área.",
        1,
        1
    ),
    (
        "Rutina de cardio",
        3,
        3,
        3,
        '2025-12-22',
        "Completar la sesión de entrenamiento aeróbico de 45 minutos programada para mantener la constancia.",
        1,
        1
    );
